"""
Resume Parser Framework that combines file parsing and field extraction.
"""

from pathlib import Path
from ..parsers.file_parser import FileParser
from ..extractors.resume_extractor import ResumeExtractor
from ..models.resume import ResumeData


class ResumeParserFramework:
    """Main framework class that combines file parsing and resume extraction."""
    
    def __init__(self, file_parser: FileParser, resume_extractor: ResumeExtractor):
        """
        Initialize the ResumeParserFramework.
        
        Args:
            file_parser: FileParser instance to parse resume files
            resume_extractor: ResumeExtractor instance to extract fields from text
        """
        self.file_parser = file_parser
        self.resume_extractor = resume_extractor
    
    def parse_resume(self, file_path: str) -> ResumeData:
        """
        Parse a resume file and extract structured resume data.
        
        Args:
            file_path: Path to the resume file as a string
        
        Returns:
            A ResumeData instance containing extracted resume information
            
        Raises:
            FileNotFoundError: If the file does not exist
            ValueError: If the file format is invalid or extraction fails
            IOError: If there's an error reading the file
        """
        path = Path(file_path)
        text = self.file_parser.parse(path)
        resume = self.resume_extractor.extract(text)
        
        return resume
