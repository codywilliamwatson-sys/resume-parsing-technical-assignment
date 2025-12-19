"""
Name field extractor implementation.
Handles extraction of candidate name from resume text.
"""

from typing import Optional

from .field_extractor import FieldExtractor
from ..llm.llm_interface import LLMInterface


class NameExtractor(FieldExtractor):
    """Extractor for candidate name from resume text."""
    
    def extract(self, text: str, llm_interface: LLMInterface) -> Optional[str]:
        """
        Extract the candidate's name from the given text.
        
        Args:
            text: The text content to extract the name from
            
        Returns:
            The extracted name, or None if the name cannot be found
            
        Raises:
            ValueError: If the input text is invalid
        """
        self.validate_text(text)

        prompt = f"You will be provided the text of a resume. Extract the name of the candidate from the text. Return only the name, no other text or formatting.\nResume text:/n{text}"
        response = llm_interface.generate_response(prompt)
        
        return response if response else None

