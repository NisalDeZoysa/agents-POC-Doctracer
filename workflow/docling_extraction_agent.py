# docling_extraction_agent.py

from pathlib import Path
import json
import time
import logging
import os
import asyncio

import httpx
from flask import Flask, request, jsonify

from docling.datamodel.base_models import InputFormat
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.pipeline_options import PdfPipelineOptions

logging.basicConfig(level=logging.INFO)
_log = logging.getLogger(__name__)

app = Flask(__name__)

# URL of your metadata agent (adjust if needed or set via env)
METADATA_AGENT_URL = os.environ.get("METADATA_AGENT_URL", "http://localhost:5030")

def extract_text_from_pdfplumber(pdf_path: str, output_dir: str = "output") -> str:
    pipeline_options = PdfPipelineOptions()
    pipeline_options.do_ocr = False
    pipeline_options.do_table_structure = True
    pipeline_options.table_structure_options.do_cell_matching = True

    doc_converter = DocumentConverter(
        allowed_formats=[InputFormat.PDF],
        format_options={InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)},
    )

    start = time.time()
    result = doc_converter.convert(pdf_path)
    _log.info(f"Conversion took {time.time() - start:.1f}s")

    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    stem = result.input.file.stem

    raw = result.document.export_to_text()
    # save artifacts
    (out / f"{stem}.txt").write_text(raw, encoding="utf-8")
    (out / f"{stem}.md").write_text(result.document.export_to_markdown(), encoding="utf-8")
    with open(out / f"{stem}.json", "w", encoding="utf-8") as f:
        json.dump(result.document.export_to_dict(), f, indent=2)

    return raw

class DoclingExtractionAgent:
    AGENT_CARD = {
        "name": "DOCLING_EXTRACTION_AGENT",
        "title": "Docling PDF Extraction Agent",
        "description": "Extract raw text from a PDF via Docling, then call the metadata agent and return both text and metadata.",
        "url": "http://localhost:5020",
        "version": "1.1",
        "capabilities": {"streaming": False, "pushNotifications": False},
    }

    async def invoke(self, pdf_path: str, task_id: str):
        # 1) Extract text
        try:
            text = extract_text_from_pdfplumber(pdf_path)
        except Exception as e:
            _log.exception("PDF extraction failed")
            return {"is_task_complete": False, "content": {"error": f"Extraction error: {e}"}}

        # 2) Call metadata agent
        try:
            async with httpx.AsyncClient() as client:
                meta_req = {"id": task_id, "message": text}
                meta_res = await client.post(f"{METADATA_AGENT_URL}/tasks/send", json=meta_req, timeout=30.0)
                meta_res.raise_for_status()
                meta_payload = meta_res.json()
        except Exception as e:
            _log.exception("Metadata agent call failed")
            return {
                "is_task_complete": False,
                "content": {
                    "extracted_text": text,
                    "metadata_error": str(e)
                }
            }

        # 3) Extract the metadata JSON from the agent response
        try:
            meta_content = meta_payload["metadata-extraction-agent"]["response"]
            metadata = meta_content.get("metadata")
        except KeyError:
            return {
                "is_task_complete": False,
                "content": {
                    "extracted_text": text,
                    "metadata_error": "Unexpected metadata-agent response format",
                    "raw_metadata_response": meta_payload
                }
            }

        # 4) Return combined result
        return {
            "is_task_complete": True,
            "content": {
                "extracted_text": text,
                "metadata": metadata
            }
        }

@app.get("/.well-known/agent.json")
def agent_card():
    return jsonify(DoclingExtractionAgent.AGENT_CARD)

@app.post("/tasks/send")
def handle_task():
    data = request.get_json() or {}
    task_id = data.get("id", "")
    pdf_path = data.get("message", "")  # expecting local path or URL

    agent = DoclingExtractionAgent()
    resp = asyncio.run(agent.invoke(pdf_path, task_id))

    key = "docling-extraction-agent"
    if not resp.get("is_task_complete", False):
        return jsonify({
            key: {"id": task_id, "status": "error", "response": resp["content"]},
            "agent_responses": data.get("agent_responses", []),
        }), 500

    return jsonify({
        key: {"id": task_id, "status": "success", "response": resp["content"]},
        "agent_responses": data.get("agent_responses", []),
    }), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5020))
    app.run(host="0.0.0.0", port=port)
