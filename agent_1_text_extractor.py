"""
Agent 1: PDF Text Extractor using Docling
Input: PDF file
Output: Structured text content
"""
from pdf_extractor import extract_text_from_pdfplumber

def agent_1_extract(pdf_path):
    structured_text = extract_text_from_pdfplumber(pdf_path)
    return structured_text