"""Abstract base class for field extractors."""

from abc import ABC, abstractmethod
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from ..llm.llm_interface import LLMInterface


class FieldExtractor(ABC):
    """Abstract base class for extracting specific fields from text."""
    
    @abstractmethod
    def extract(self, text: str, llm_interface: 'LLMInterface'):
        """
        Extract a specific field from the given text.
        
        Args:
            text: The text content to extract the field from
            llm_interface: The LLM interface to use for extraction
            
        Returns:
            The extracted field value (type depends on the specific extractor),
            or None if the field cannot be found
            
        Raises:
            ValueError: If the input text is invalid
        """
        pass  # pragma: no cover
    
    def validate_text(self, text: str) -> None:
        """Validate that the input text is valid for extraction."""
        if text is None:
            raise ValueError("Text cannot be None")
        
        if not isinstance(text, str):
            raise ValueError(f"Text must be a string, got {type(text).__name__}")
        
        if not text.strip():
            raise ValueError("Text cannot be empty or whitespace only")

