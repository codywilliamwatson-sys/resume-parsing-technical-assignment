"""
Resume data class.
Encapsulates resume information extracted from parsed documents.
"""

from dataclasses import dataclass, field
from typing import List


@dataclass
class ResumeData:
    """
    Data class representing a parsed resume.
    
    Attributes:
        name: The candidate's name
        email: The candidate's email address
        skills: List of skills possessed by the candidate
    """
    
    name: str
    email: str
    skills: List[str] = field(default_factory=list)
