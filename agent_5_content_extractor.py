"""
Agent 5: Extract basic structure of each amendment (headings, types, purview, subjects)
"""
from prompt_catalog import PromptCatalog

def agent_5_extract_structure(block: str, llm_generate) -> dict:
    prompt = PromptCatalog.CHANGES_STRUCTURE_EXTRACTION.format(gazette_text=block)
    return llm_generate(prompt)