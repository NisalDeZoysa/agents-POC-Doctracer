"""
Agent 6: Extract departmental/institutional/legal data from structured text or table-like blocks
"""
from prompt_catalog import PromptCatalog

def agent_6_extract_tables(block: str, llm_generate) -> dict:
    prompt = PromptCatalog.CHANGES_TABLE_EXTRACTION_FROM_TEXT.format(gazette_text=block)
    return llm_generate(prompt)