"""
PromptCatalog contains all prompt templates used by the agents.
"""
class PromptCatalog:
    METADATA_EXTRACTION = """
        You are an assistant tasked with extracting metadata from a government gazette document. Using the provided text, identify and return the following information in a compact JSON string:
        - Gazette ID
        - Gazette Published Date
        - Gazette Published by whom
        Ensure the JSON string is compact.
        Input Text:
        {gazette_text}
    """

    CHANGES_OPERATION_TYPE_IDENTIFICATION = """
        Extract each amendment block and identify its operation type (INSERTION, DELETION, UPDATE, RENUMBERING, or OTHER). Return a JSON list of blocks like:
        [
          {"operation_type": "INSERTION", "text": "<amendment block text>"},
          ...
        ]
        Input:
        {gazette_text}
    """

    CHANGES_STRUCTURE_EXTRACTION = """
        Extract core content from this amendment block:
        - heading_number
        - heading_name
        - purview
        - subjects_and_functions
        - special_priorities
        Return as: {"details": {<fields>}}
        Input:
        {gazette_text}
    """

    CHANGES_TABLE_EXTRACTION_FROM_TEXT = """
        Extract ministers and their associated departments, laws, and functions from text-formatted tables.
        Return as JSON:
        {
          "departments_and_institutions": [...],
          "laws_and_ordinances": [...]
        }
        Input:
        {gazette_text}
    """
