"""
Resume extractor that orchestrates multiple field extractors
to create a complete ResumeData instance.
"""

from typing import Dict, Optional
from .field_extractor import FieldExtractor
from ..models.resume import ResumeData
from ..llm.llm_interface import LLMInterface


class ResumeExtractor:
    """Orchestrates multiple field extractors to create a ResumeData instance."""
    
    def __init__(self, extractors: Dict[str, FieldExtractor], llm_interface: LLMInterface):
        """
        Initialize the ResumeExtractor with a dictionary of field extractors and an LLM interface.
        
        Args:
            extractors: Dictionary mapping field names to FieldExtractor instances.
                      Expected keys: 'name', 'email', 'skills'
            llm_interface: LLM interface to use for field extraction
        
        Raises:
            ValueError: If extractors dictionary is empty
        """
        if not extractors:
            raise ValueError("Extractors dictionary cannot be empty")
        self.extractors = extractors
        self.llm_interface = llm_interface
    
    def extract(self, text: str) -> ResumeData:
        """
        Extract all resume fields from the given text and create a ResumeData instance.
        
        Args:
            text: The text content to extract resume information from
        
        Returns:
            A ResumeData instance with extracted fields
            
        Raises:
            ValueError: If the input text is invalid
        """
        if not text or not isinstance(text, str) or not text.strip():
            raise ValueError("Text cannot be empty or None")
        
        extracted_fields = {}
        for field_name, extractor in self.extractors.items():
            extracted_value = extractor.extract(text, self.llm_interface)
            extracted_fields[field_name] = extracted_value
        
        # Handle None values - convert to defaults
        name = extracted_fields.get('name')
        if name is None:
            name = ''
        
        email = extracted_fields.get('email')
        if email is None:
            email = ''
        
        skills = extracted_fields.get('skills')
        if skills is None:
            skills = []
        
        return ResumeData(
            name=name,
            email=email,
            skills=skills
        )

