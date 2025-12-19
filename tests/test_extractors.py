"""Tests for field extractors."""

import pytest
from unittest.mock import Mock, patch
from typing import List

from src.extractors.name_extractor import NameExtractor
from src.extractors.email_extractor import EmailExtractor
from src.extractors.skills_extractor import SkillsExtractor
from src.extractors.resume_extractor import ResumeExtractor
from src.extractors.field_extractor import FieldExtractor
from src.models.resume import ResumeData


class TestNameExtractor:
    """Test cases for NameExtractor."""
    
    def test_init(self):
        """Test NameExtractor initialization."""
        extractor = NameExtractor()
        assert isinstance(extractor, FieldExtractor)
    
    def test_validate_text_none(self):
        """Test validate_text raises ValueError for None."""
        extractor = NameExtractor()
        
        with pytest.raises(ValueError, match="Text cannot be None"):
            extractor.validate_text(None)
    
    def test_validate_text_not_string(self):
        """Test validate_text raises ValueError for non-string."""
        extractor = NameExtractor()
        
        with pytest.raises(ValueError, match="Text must be a string"):
            extractor.validate_text(123)
        
        # Test with different non-string types to ensure full coverage
        with pytest.raises(ValueError, match="Text must be a string"):
            extractor.validate_text([])
        with pytest.raises(ValueError, match="Text must be a string"):
            extractor.validate_text({})
    
    def test_validate_text_empty(self):
        """Test validate_text raises ValueError for empty string."""
        extractor = NameExtractor()
        
        with pytest.raises(ValueError, match="Text cannot be empty"):
            extractor.validate_text("")
        with pytest.raises(ValueError, match="Text cannot be empty"):
            extractor.validate_text("   ")
    
    def test_extract_success(self):
        """Test successful name extraction."""
        extractor = NameExtractor()
        mock_llm = Mock()
        mock_llm.generate_response.return_value = "John Doe"
        
        result = extractor.extract("Resume text here", mock_llm)
        
        assert result == "John Doe"
        mock_llm.generate_response.assert_called_once()
    
    def test_extract_returns_none_when_empty_response(self):
        """Test extract returns None when LLM returns empty response."""
        extractor = NameExtractor()
        mock_llm = Mock()
        mock_llm.generate_response.return_value = ""
        
        result = extractor.extract("Resume text here", mock_llm)
        
        assert result is None


class TestEmailExtractor:
    """Test cases for EmailExtractor."""
    
    def test_init(self):
        """Test EmailExtractor initialization."""
        extractor = EmailExtractor()
        assert isinstance(extractor, FieldExtractor)
    
    def test_extract_success(self):
        """Test successful email extraction."""
        extractor = EmailExtractor()
        mock_llm = Mock()
        mock_llm.generate_response.return_value = "john.doe@example.com"
        
        result = extractor.extract("Resume text here", mock_llm)
        
        assert result == "john.doe@example.com"
        mock_llm.generate_response.assert_called_once()
    
    def test_extract_returns_none_when_empty_response(self):
        """Test extract returns None when LLM returns empty response."""
        extractor = EmailExtractor()
        mock_llm = Mock()
        mock_llm.generate_response.return_value = ""
        
        result = extractor.extract("Resume text here", mock_llm)
        
        assert result is None


class TestSkillsExtractor:
    """Test cases for SkillsExtractor."""
    
    def test_init(self):
        """Test SkillsExtractor initialization."""
        extractor = SkillsExtractor()
        assert isinstance(extractor, FieldExtractor)
    
    def test_extract_success(self):
        """Test successful skills extraction."""
        extractor = SkillsExtractor()
        mock_llm = Mock()
        mock_llm.generate_response.return_value = "Python,Java,SQL"
        
        result = extractor.extract("Resume text here", mock_llm)
        
        assert result == ["Python", "Java", "SQL"]
        mock_llm.generate_response.assert_called_once()
    
    def test_extract_with_spaces(self):
        """Test skills extraction handles spaces correctly."""
        extractor = SkillsExtractor()
        mock_llm = Mock()
        mock_llm.generate_response.return_value = "Python, Java, SQL"
        
        result = extractor.extract("Resume text here", mock_llm)
        
        assert result == ["Python", "Java", "SQL"]
    
    def test_extract_returns_none_when_empty_response(self):
        """Test extract returns None when LLM returns empty response."""
        extractor = SkillsExtractor()
        mock_llm = Mock()
        mock_llm.generate_response.return_value = ""
        
        result = extractor.extract("Resume text here", mock_llm)
        
        assert result is None
    
    def test_extract_single_skill(self):
        """Test skills extraction with single skill."""
        extractor = SkillsExtractor()
        mock_llm = Mock()
        mock_llm.generate_response.return_value = "Python"
        
        result = extractor.extract("Resume text here", mock_llm)
        
        assert result == ["Python"]


class TestResumeExtractor:
    """Test cases for ResumeExtractor."""
    
    def test_init_success(self):
        """Test ResumeExtractor initialization with valid extractors."""
        mock_llm = Mock()
        extractors = {
            'name': NameExtractor(),
            'email': EmailExtractor(),
            'skills': SkillsExtractor()
        }
        
        resume_extractor = ResumeExtractor(extractors, mock_llm)
        
        assert resume_extractor.extractors == extractors
        assert resume_extractor.llm_interface == mock_llm
    
    def test_init_empty_extractors(self):
        """Test ResumeExtractor initialization raises ValueError for empty extractors."""
        mock_llm = Mock()
        
        with pytest.raises(ValueError, match="Extractors dictionary cannot be empty"):
            ResumeExtractor({}, mock_llm)
    
    def test_extract_success(self):
        """Test successful resume extraction."""
        mock_llm = Mock()
        
        mock_name_extractor = Mock()
        mock_name_extractor.extract.return_value = "John Doe"
        
        mock_email_extractor = Mock()
        mock_email_extractor.extract.return_value = "john.doe@example.com"
        
        mock_skills_extractor = Mock()
        mock_skills_extractor.extract.return_value = ["Python", "Java"]
        
        extractors = {
            'name': mock_name_extractor,
            'email': mock_email_extractor,
            'skills': mock_skills_extractor
        }
        
        resume_extractor = ResumeExtractor(extractors, mock_llm)
        result = resume_extractor.extract("Resume text here")
        
        assert isinstance(result, ResumeData)
        assert result.name == "John Doe"
        assert result.email == "john.doe@example.com"
        assert result.skills == ["Python", "Java"]
        
        mock_name_extractor.extract.assert_called_once_with("Resume text here", mock_llm)
        mock_email_extractor.extract.assert_called_once_with("Resume text here", mock_llm)
        mock_skills_extractor.extract.assert_called_once_with("Resume text here", mock_llm)
    
    def test_extract_with_missing_fields(self):
        """Test extract handles missing fields with defaults."""
        mock_llm = Mock()
        
        mock_name_extractor = Mock()
        mock_name_extractor.extract.return_value = "John Doe"
        
        mock_email_extractor = Mock()
        mock_email_extractor.extract.return_value = "john.doe@example.com"
        
        mock_skills_extractor = Mock()
        mock_skills_extractor.extract.return_value = None
        
        extractors = {
            'name': mock_name_extractor,
            'email': mock_email_extractor,
            'skills': mock_skills_extractor
        }
        
        resume_extractor = ResumeExtractor(extractors, mock_llm)
        result = resume_extractor.extract("Resume text here")
        
        assert result.name == "John Doe"
        assert result.email == "john.doe@example.com"
        assert result.skills == []
    
    def test_extract_with_missing_name(self):
        """Test extract handles None name with default."""
        mock_llm = Mock()
        
        mock_name_extractor = Mock()
        mock_name_extractor.extract.return_value = None
        
        mock_email_extractor = Mock()
        mock_email_extractor.extract.return_value = "john.doe@example.com"
        
        mock_skills_extractor = Mock()
        mock_skills_extractor.extract.return_value = ["Python"]
        
        extractors = {
            'name': mock_name_extractor,
            'email': mock_email_extractor,
            'skills': mock_skills_extractor
        }
        
        resume_extractor = ResumeExtractor(extractors, mock_llm)
        result = resume_extractor.extract("Resume text here")
        
        assert result.name == ""
        assert result.email == "john.doe@example.com"
        assert result.skills == ["Python"]
    
    def test_extract_with_missing_email(self):
        """Test extract handles None email with default."""
        mock_llm = Mock()
        
        mock_name_extractor = Mock()
        mock_name_extractor.extract.return_value = "John Doe"
        
        mock_email_extractor = Mock()
        mock_email_extractor.extract.return_value = None
        
        mock_skills_extractor = Mock()
        mock_skills_extractor.extract.return_value = ["Python"]
        
        extractors = {
            'name': mock_name_extractor,
            'email': mock_email_extractor,
            'skills': mock_skills_extractor
        }
        
        resume_extractor = ResumeExtractor(extractors, mock_llm)
        result = resume_extractor.extract("Resume text here")
        
        assert result.name == "John Doe"
        assert result.email == ""
        assert result.skills == ["Python"]
    
    def test_extract_empty_text(self):
        """Test extract raises ValueError for empty text."""
        mock_llm = Mock()
        extractors = {
            'name': NameExtractor(),
            'email': EmailExtractor(),
            'skills': SkillsExtractor()
        }
        
        resume_extractor = ResumeExtractor(extractors, mock_llm)
        
        with pytest.raises(ValueError, match="Text cannot be empty"):
            resume_extractor.extract("")
    
    def test_extract_none_text(self):
        """Test extract raises ValueError for None text."""
        mock_llm = Mock()
        extractors = {
            'name': NameExtractor(),
            'email': EmailExtractor(),
            'skills': SkillsExtractor()
        }
        
        resume_extractor = ResumeExtractor(extractors, mock_llm)
        
        with pytest.raises(ValueError, match="Text cannot be empty"):
            resume_extractor.extract(None)
    
    def test_extract_whitespace_only_text(self):
        """Test extract raises ValueError for whitespace-only text."""
        mock_llm = Mock()
        extractors = {
            'name': NameExtractor(),
            'email': EmailExtractor(),
            'skills': SkillsExtractor()
        }
        
        resume_extractor = ResumeExtractor(extractors, mock_llm)
        
        with pytest.raises(ValueError, match="Text cannot be empty"):
            resume_extractor.extract("   ")
    
    def test_extract_with_additional_extractors(self):
        """Test extract works with additional extractors beyond required fields."""
        mock_llm = Mock()
        
        mock_name_extractor = Mock()
        mock_name_extractor.extract.return_value = "John Doe"
        
        mock_email_extractor = Mock()
        mock_email_extractor.extract.return_value = "john.doe@example.com"
        
        mock_skills_extractor = Mock()
        mock_skills_extractor.extract.return_value = ["Python"]
        
        mock_phone_extractor = Mock()
        mock_phone_extractor.extract.return_value = "123-456-7890"
        
        extractors = {
            'name': mock_name_extractor,
            'email': mock_email_extractor,
            'skills': mock_skills_extractor,
            'phone': mock_phone_extractor
        }
        
        resume_extractor = ResumeExtractor(extractors, mock_llm)
        result = resume_extractor.extract("Resume text here")
        
        # Should still create ResumeData with default values for phone
        assert result.name == "John Doe"
        assert result.email == "john.doe@example.com"
        assert result.skills == ["Python"]

