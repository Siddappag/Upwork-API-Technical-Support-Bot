"""
Document Loader Module
Handles loading and preprocessing of PDF documents
"""

from pypdf import PdfReader
from typing import Tuple


def load_pdf(pdf_path: str) -> str:
    """
    Load PDF file and extract text.
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        Extracted text from PDF
    """
    pdf_reader = PdfReader(pdf_path)
    text = ""
    
    for page in pdf_reader.pages:
        text += page.extract_text()
    
    return text


def perform_sanity_check(text: str) -> Tuple[int, str]:
    """
    Perform sanity check on loaded document.
    
    Args:
        text: Loaded document text
        
    Returns:
        Tuple of (character_count, first_500_chars)
    """
    char_count = len(text)
    first_500 = text[:500]
    
    return char_count, first_500
