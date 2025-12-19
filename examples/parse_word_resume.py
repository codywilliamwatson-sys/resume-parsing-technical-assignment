"""Example: Parse a Word resume file."""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.framework import ResumeParserFramework
from src.parsers import WordParser
from src.extractors import ResumeExtractor, NameExtractor, EmailExtractor, SkillsExtractor
from src.llm import GeminiLLM


def main():
    """Parse a Word resume and extract structured data."""
    # Initialize LLM
    llm = GeminiLLM()
    
    # Create extractors
    extractors = {
        'name': NameExtractor(),
        'email': EmailExtractor(),
        'skills': SkillsExtractor()
    }
    
    # Create resume extractor
    resume_extractor = ResumeExtractor(extractors, llm)
    
    # Create Word parser
    word_parser = WordParser()
    
    # Create framework
    framework = ResumeParserFramework(word_parser, resume_extractor)
    
    # Get path to sample resume
    examples_dir = Path(__file__).parent
    resume_path = examples_dir / 'sample_resumes' / 'sample_resume.docx'
    
    # Parse resume
    resume_data = framework.parse_resume(str(resume_path))
    
    print(f"Name: {resume_data.name}")
    print(f"Email: {resume_data.email}")
    print(f"Skills: {resume_data.skills}")


if __name__ == '__main__':
    main()

