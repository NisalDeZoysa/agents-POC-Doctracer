"""
Agent 4: Identify amendment blocks and classify operation type
Output: List of amendment blocks with operation type tagged
"""
from prompt_catalog import PromptCatalog

def agent_4_identify_operations(text: str, llm_generate) -> list:
    prompt = PromptCatalog.CHANGES_OPERATION_TYPE_IDENTIFICATION.format(gazette_text=text)
    return llm_generate(prompt)