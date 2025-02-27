"""
Text extraction module for different file types
"""

import os
import logging
from io import BytesIO

# For PDF processing
from pdfminer.high_level import extract_text as extract_text_pdf

# For DOCX processing
import mammoth

from app.utils import cleanup_text

logger = logging.getLogger('resume_matcher.core.extractor')

def extract_text_from_file(file_path):
    """
    Extract text from a file based on its extension
    
    Args:
        file_path (str): Path to the file
        
    Returns:
        str: Extracted text from the file
        
    Raises:
        ValueError: If file format is not supported
        FileNotFoundError: If file does not exist
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    _, file_ext = os.path.splitext(file_path)
    file_ext = file_ext.lower()
    
    logger.info(f"Extracting text from: {os.path.basename(file_path)}")
    
    if file_ext == '.pdf':
        return extract_text_from_pdf(file_path)
    elif file_ext == '.docx':
        return extract_text_from_docx(file_path)
    else:
        raise ValueError(f"Unsupported file format: {file_ext}")

def extract_text_from_pdf(file_path):
    """
    Extract text from a PDF file
    
    Args:
        file_path (str): Path to the PDF file
        
    Returns:
        str: Extracted text from the PDF
    """
    try:
        text = extract_text_pdf(file_path)
        return cleanup_text(text)
    except Exception as e:
        logger.error(f"Error extracting text from PDF: {e}")
        raise

def extract_text_from_docx(file_path):
    """
    Extract text from a DOCX file
    
    Args:
        file_path (str): Path to the DOCX file
        
    Returns:
        str: Extracted text from the DOCX
    """
    try:
        with open(file_path, 'rb') as docx_file:
            result = mammoth.extract_raw_text(docx_file)
            return cleanup_text(result.value)
    except Exception as e:
        logger.error(f"Error extracting text from DOCX: {e}")
        raise