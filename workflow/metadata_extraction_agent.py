# metadata_extraction_agent.py

import os
import json
import asyncio
from pathlib import Path
from flask import Flask, request, jsonify
from langchain_ollama import ChatOllama

app = Flask(__name__)

# Your prompt template
_METADATA_PROMPT_TEMPLATE: str = """
You are an assistant tasked with extracting metadata from a government gazette document. 
Using the provided text, identify and return the following information in a compact JSON string:
- Gazette ID
- Gazette Published Date
- Gazette Published by whom

Ensure the JSON string is compact, without any additional formatting or escape characters.
Don't include unnecessary backward slashes or forward slashes unless the data contains them. 

Input Text:
{gazette_text}

Sample JSON Output:
{{"Gazette ID":"2303/17","Gazette Published Date":"2022-10-26","Gazette Published by":"Authority"}}
"""

class MetadataExtractionAgent:
    AGENT_CARD = {
        "name": "METADATA_EXTRACTION_AGENT",
        "title": "Gazette Metadata Extraction Agent",
        "description": "Extract Gazette ID, published date, and publisher from gazette text.",
        "url": "http://localhost:5030",
        "version": "1.0",
        "capabilities": {"streaming": False, "pushNotifications": False},
    }

    def __init__(self):
        self.llm = ChatOllama(model="gpt-4o-mini:latest", temperature=0.0)

    async def invoke(self, gazette_text: str, task_id: str):
        prompt = _METADATA_PROMPT_TEMPLATE.format(gazette_text=gazette_text)
        # Single‐shot chat
        resp = await self.llm.apredict_messages([{"role": "user", "content": prompt}])
        metadata_str = resp.content.strip()

        # Parse into dict
        try:
            metadata_dict = json.loads(metadata_str)
        except json.JSONDecodeError:
            # If parsing fails, return error
            return {"is_task_complete": False, "content": {"error": "LLM did not return valid JSON"}}

        # Write out to file
        out_dir = Path("output")
        out_dir.mkdir(exist_ok=True)
        file_path = out_dir / f"{task_id}.json"
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(metadata_dict, f, ensure_ascii=False, indent=2)

        return {
            "is_task_complete": True,
            "content": {
                "metadata": metadata_dict,
                "output_path": str(file_path)
            }
        }

@app.get("/.well-known/agent.json")
def agent_card():
    return jsonify(MetadataExtractionAgent.AGENT_CARD)

@app.post("/tasks/send")
def handle_task():
    data = request.get_json() or {}
    task_id = data.get("id", "")
    gazette_text = data.get("message", "")
    agent = MetadataExtractionAgent()
    resp = asyncio.run(agent.invoke(gazette_text, task_id))

    key = "metadata-extraction-agent"
    if not resp.get("is_task_complete", False):
        out = {
            key: {"id": task_id, "status": "error", "response": resp["content"]},
            "agent_responses": data.get("agent_responses", []),
        }
        return jsonify(out), 500

    out = {
        key: {"id": task_id, "status": "success", "response": resp["content"]},
        "agent_responses": data.get("agent_responses", []),
    }
    return jsonify(out), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5030))
    app.run(host="0.0.0.0", port=port)
