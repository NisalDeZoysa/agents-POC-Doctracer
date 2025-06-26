
# agent_3_metadata_extractor.py
"""
Agent 3: Metadata Extractor
Input: Metadata text
Output: Metadata dictionary using prompt-based LLM call
"""
from prompt_catalog import PromptCatalog

def agent_3_metadata(text: str, llm_generate) -> dict:
    prompt = PromptCatalog.METADATA_EXTRACTION.format(gazette_text=text)
    return llm_generate(prompt)
