"""
PDF extraction and text processing service.
"""
import PyPDF2
from typing import List, Tuple
import logging

logger = logging.getLogger(__name__)


class PDFExtractionService:
    """Service for extracting text from PDF files."""
    
    @staticmethod
    def extract_text(pdf_path: str) -> Tuple[str, int]:
        """
        Extract text from a PDF file.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Tuple of (extracted_text, page_count)
            
        Raises:
            ValueError: If PDF cannot be read
        """
        try:
            text = ""
            page_count = 0
            
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                page_count = len(reader.pages)
                
                for page in reader.pages:
                    text += page.extract_text() + "\n"
            
            if not text.strip():
                raise ValueError("No text extracted from PDF")
            
            logger.info(f"Successfully extracted text from {page_count} pages")
            return text, page_count
            
        except Exception as e:
            logger.error(f"Error extracting PDF text: {str(e)}")
            raise ValueError(f"Failed to extract text from PDF: {str(e)}")
    
    @staticmethod
    def validate_pdf(file_path: str) -> bool:
        """
        Validate if file is a valid PDF.
        
        Args:
            file_path: Path to the file
            
        Returns:
            True if valid PDF, False otherwise
        """
        try:
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                return len(reader.pages) > 0
        except Exception as e:
            logger.error(f"PDF validation error: {str(e)}")
            return False
