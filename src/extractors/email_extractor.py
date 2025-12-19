"""
Email field extractor implementation.
Handles extraction of email address from resume text.
"""

from typing import Optional

from .field_extractor import FieldExtractor
from ..llm.llm_interface import LLMInterface


class EmailExtractor(FieldExtractor):
    """Extractor for email address from resume text."""
    
    def extract(self, text: str, llm_interface: LLMInterface) -> Optional[str]:
        """
        Extract the email address from the given text.
        
        Args:
            text: The text content to extract the email from
            llm_interface: The LLM interface to use for extraction
            
        Returns:
            The extracted email address, or None if the email cannot be found
            
        Raises:
            ValueError: If the input text is invalid
        """
        self.validate_text(text)
        
        prompt = f"You will be provided the text of a resume. Extract the email address from the text. Return only the email address, no other text or formatting.\nResume text:/n{text}"
        response = llm_interface.generate_response(prompt)
        
        return response if response else None

