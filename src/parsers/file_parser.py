"""Abstract base class for file parsers."""

from abc import ABC, abstractmethod
from pathlib import Path


class FileParser(ABC):
    """Abstract base class for parsing files."""
    
    @abstractmethod
    def parse(self, file_path: Path) -> str:
        """
        Parse a file and extract text content.
        
        Args:
            file_path: Path to the file to be parsed
            
        Returns:
            String containing the extracted text content
            
        Raises:
            FileNotFoundError: If the file does not exist
            ValueError: If the file format is invalid or unsupported
            IOError: If there's an error reading the file
        """
        pass  # pragma: no cover
    
    @abstractmethod
    def can_parse(self, file_path: Path) -> bool:
        """
        Check if this parser can handle the given file.
        
        Args:
            file_path: Path to the file to check
            
        Returns:
            True if this parser can parse the file, False otherwise
        """
        pass  # pragma: no cover
    
    @abstractmethod
    def get_supported_extensions(self) -> list[str]:
        """
        Get the list of file extensions this parser supports.
        
        Returns:
            List of supported file extensions (e.g., ['.pdf', '.docx'])
        """
        pass  # pragma: no cover
    
    def validate_file(self, file_path: Path) -> None:
        """Validate that the file exists and is readable."""
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        if not file_path.is_file():
            raise ValueError(f"Path is not a file: {file_path}")
        
        if not file_path.stat().st_size > 0:
            raise ValueError(f"File is empty: {file_path}")

