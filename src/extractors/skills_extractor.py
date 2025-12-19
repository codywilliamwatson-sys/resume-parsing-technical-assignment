"""
Skills field extractor implementation.
Handles extraction of skills from resume text.
"""

from typing import Optional, List

from .field_extractor import FieldExtractor
from ..llm.llm_interface import LLMInterface


class SkillsExtractor(FieldExtractor):
    """Extractor for skills from resume text."""
    
    def extract(self, text: str, llm_interface: LLMInterface) -> Optional[List[str]]:
        """
        Extract skills from the given text.
        
        Args:
            text: The text content to extract skills from
            
        Returns:
            The extracted skills (comma-separated or formatted string), 
            or None if skills cannot be found
            
        Raises:
            ValueError: If the input text is invalid
        """
        self.validate_text(text)

        prompt = f"You will be provided the text of a resume. Extract the skills of the candidate from the text. Return only the skills separated by commas with no spaces, no other text or formatting.Here is an example of the expected format: 'Python,Java,SQL'\nResume text:/n{text}"
        response = llm_interface.generate_response(prompt)

        return [skill.strip() for skill in response.split(',')] if response else None

