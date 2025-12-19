"""
PDF file parser implementation.
Handles parsing of PDF resume files.
"""

from pathlib import Path
import pypdf

from .file_parser import FileParser


class PDFParser(FileParser):
    """Parser for PDF files."""
    
    def __init__(self):
        """Initialize the PDF parser."""
        self._supported_extensions = ['.pdf']
    
    def parse(self, file_path: Path) -> str:
        """
        Parse a PDF file and extract text content.
        
        Args:
            file_path: Path to the PDF file to be parsed
            
        Returns:
            String containing the extracted text content from all pages
            
        Raises:
            FileNotFoundError: If the file does not exist
            ValueError: If the file format is invalid or unsupported
            IOError: If there's an error reading the file
        """
        self.validate_file(file_path)
        
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = pypdf.PdfReader(file)
                
                text_content = []
                for page in pdf_reader.pages:
                    text_content.append(page.extract_text())
                
                return '\n'.join(text_content)
        except pypdf.errors.PdfReadError as e:
            raise ValueError(f"Invalid PDF file: {file_path}") from e
        except Exception as e:
            raise IOError(f"Error reading PDF file: {file_path}") from e
    
    def can_parse(self, file_path: Path) -> bool:
        """
        Check if this parser can handle the given file.
        
        Args:
            file_path: Path to the file to check
            
        Returns:
            True if the file has a .pdf extension, False otherwise
        """
        return file_path.suffix.lower() in self._supported_extensions
    
    def get_supported_extensions(self) -> list[str]:
        """
        Get the list of file extensions this parser supports.
        
        Returns:
            List containing ['.pdf']
        """
        return self._supported_extensions.copy()
    

