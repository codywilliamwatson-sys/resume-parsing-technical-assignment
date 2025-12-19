"""Tests for ResumeData model."""

import pytest
from src.models.resume import ResumeData


class TestResumeData:
    """Test cases for ResumeData dataclass."""
    
    def test_resume_data_creation_with_all_fields(self):
        """Test creating ResumeData with all fields."""
        resume = ResumeData(
            name="John Doe",
            email="john.doe@example.com",
            skills=["Python", "Java", "SQL"]
        )
        
        assert resume.name == "John Doe"
        assert resume.email == "john.doe@example.com"
        assert resume.skills == ["Python", "Java", "SQL"]
    
    def test_resume_data_creation_with_default_skills(self):
        """Test creating ResumeData with default empty skills list."""
        resume = ResumeData(
            name="Jane Smith",
            email="jane.smith@example.com"
        )
        
        assert resume.name == "Jane Smith"
        assert resume.email == "jane.smith@example.com"
        assert resume.skills == []
    
    def test_resume_data_equality(self):
        """Test ResumeData equality comparison."""
        resume1 = ResumeData(
            name="John Doe",
            email="john.doe@example.com",
            skills=["Python"]
        )
        resume2 = ResumeData(
            name="John Doe",
            email="john.doe@example.com",
            skills=["Python"]
        )
        
        assert resume1 == resume2
    
    def test_resume_data_inequality(self):
        """Test ResumeData inequality comparison."""
        resume1 = ResumeData(
            name="John Doe",
            email="john.doe@example.com",
            skills=["Python"]
        )
        resume2 = ResumeData(
            name="Jane Smith",
            email="jane.smith@example.com",
            skills=["Java"]
        )
        
        assert resume1 != resume2

