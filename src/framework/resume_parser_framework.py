"""
Resume Parser Framework that combines file parsing and field extraction.
"""

import logging
from pathlib import Path
from typing import List, Optional
from ..parsers.file_parser import FileParser
from ..parsers.pdf_parser import PDFParser
from ..parsers.word_parser import WordParser
from ..extractors.resume_extractor import ResumeExtractor
from ..models.resume import ResumeData

logger = logging.getLogger(__name__)


class ResumeParserFramework:
    """Main framework class that combines file parsing and resume extraction."""
    
    def __init__(self, resume_extractor: ResumeExtractor, parsers: Optional[List[FileParser]] = None):
        """
        Initialize the ResumeParserFramework.
        
        Args:
            resume_extractor: ResumeExtractor instance to extract fields from text
            parsers: Optional list of FileParser instances. If not provided, defaults to
                    [PDFParser(), WordParser()]
        
        Raises:
            ValueError: If parsers list is empty
        """
        if parsers is None:
            parsers = [PDFParser(), WordParser()]
        
        if not parsers:
            raise ValueError("Parsers list cannot be empty")
        
        self.parsers = parsers
        self.resume_extractor = resume_extractor
        logger.debug(f"Initialized ResumeParserFramework with {len(parsers)} parsers")
    
    def _select_parser(self, file_path: Path) -> FileParser:
        """
        Select the appropriate parser for the given file based on its extension.
        
        Args:
            file_path: Path to the file to parse
        
        Returns:
            A FileParser instance that can handle the file
            
        Raises:
            ValueError: If no parser can handle the file extension
        """
        for parser in self.parsers:
            if parser.can_parse(file_path):
                logger.debug(f"Selected parser: {type(parser).__name__} for file: {file_path}")
                return parser
        
        supported_extensions = []
        for parser in self.parsers:
            supported_extensions.extend(parser.get_supported_extensions())
        raise ValueError(
            f"No parser available for file extension '{file_path.suffix}'. "
            f"Supported extensions: {', '.join(set(supported_extensions))}"
        )
    
    def parse_resume(self, file_path: str) -> ResumeData:
        """
        Parse a resume file and extract structured resume data.
        Automatically selects the appropriate parser based on file extension.
        
        Args:
            file_path: Path to the resume file as a string
        
        Returns:
            A ResumeData instance containing extracted resume information
            
        Raises:
            FileNotFoundError: If the file does not exist
            ValueError: If the file format is invalid, unsupported, or extraction fails
            IOError: If there's an error reading the file
        """
        logger.info(f"Starting resume parsing for file: {file_path}")
        path = Path(file_path)
        
        file_parser = self._select_parser(path)
        text = file_parser.parse(path)
        logger.debug(f"Extracted {len(text)} characters from file")
        resume = self.resume_extractor.extract(text)
        logger.info(f"Successfully parsed resume")
        
        return resume
