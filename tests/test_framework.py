"""Tests for ResumeParserFramework."""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch

from src.framework.resume_parser_framework import ResumeParserFramework
from src.parsers.pdf_parser import PDFParser
from src.parsers.word_parser import WordParser
from src.extractors.resume_extractor import ResumeExtractor
from src.extractors.name_extractor import NameExtractor
from src.extractors.email_extractor import EmailExtractor
from src.extractors.skills_extractor import SkillsExtractor
from src.models.resume import ResumeData


class TestResumeParserFramework:
    """Test cases for ResumeParserFramework."""
    
    def test_init(self):
        """Test ResumeParserFramework initialization."""
        mock_parser = Mock()
        mock_extractor = Mock()
        
        framework = ResumeParserFramework(mock_parser, mock_extractor)
        
        assert framework.file_parser == mock_parser
        assert framework.resume_extractor == mock_extractor
    
    def test_parse_resume_success(self, tmp_path):
        """Test successful resume parsing."""
        # Setup
        file_path = tmp_path / "resume.pdf"
        file_path.write_bytes(b"fake pdf content")
        
        mock_parser = Mock()
        mock_parser.parse.return_value = "Resume text content"
        
        mock_llm = Mock()
        extractors = {
            'name': NameExtractor(),
            'email': EmailExtractor(),
            'skills': SkillsExtractor()
        }
        
        mock_name_extractor = Mock()
        mock_name_extractor.extract.return_value = "John Doe"
        
        mock_email_extractor = Mock()
        mock_email_extractor.extract.return_value = "john.doe@example.com"
        
        mock_skills_extractor = Mock()
        mock_skills_extractor.extract.return_value = ["Python", "Java"]
        
        extractors_mock = {
            'name': mock_name_extractor,
            'email': mock_email_extractor,
            'skills': mock_skills_extractor
        }
        
        resume_extractor = ResumeExtractor(extractors_mock, mock_llm)
        
        framework = ResumeParserFramework(mock_parser, resume_extractor)
        
        # Execute
        result = framework.parse_resume(str(file_path))
        
        # Assert
        assert isinstance(result, ResumeData)
        assert result.name == "John Doe"
        assert result.email == "john.doe@example.com"
        assert result.skills == ["Python", "Java"]
        mock_parser.parse.assert_called_once_with(Path(file_path))
    
    def test_parse_resume_file_not_found(self):
        """Test parse_resume raises FileNotFoundError for non-existent file."""
        mock_parser = Mock()
        mock_parser.parse.side_effect = FileNotFoundError("File not found")
        
        mock_extractor = Mock()
        
        framework = ResumeParserFramework(mock_parser, mock_extractor)
        
        with pytest.raises(FileNotFoundError):
            framework.parse_resume("nonexistent.pdf")
    
    def test_parse_resume_invalid_format(self):
        """Test parse_resume raises ValueError for invalid file format."""
        mock_parser = Mock()
        mock_parser.parse.side_effect = ValueError("Invalid file format")
        
        mock_extractor = Mock()
        
        framework = ResumeParserFramework(mock_parser, mock_extractor)
        
        with pytest.raises(ValueError):
            framework.parse_resume("invalid.pdf")
    
    def test_parse_resume_io_error(self):
        """Test parse_resume raises IOError for file read errors."""
        mock_parser = Mock()
        mock_parser.parse.side_effect = IOError("Cannot read file")
        
        mock_extractor = Mock()
        
        framework = ResumeParserFramework(mock_parser, mock_extractor)
        
        with pytest.raises(IOError):
            framework.parse_resume("test.pdf")
    
    def test_parse_resume_extraction_failure(self):
        """Test parse_resume handles extraction failures."""
        mock_parser = Mock()
        mock_parser.parse.return_value = "Resume text"
        
        mock_extractor = Mock()
        mock_extractor.extract.side_effect = ValueError("Extraction failed")
        
        framework = ResumeParserFramework(mock_parser, mock_extractor)
        
        with pytest.raises(ValueError, match="Extraction failed"):
            framework.parse_resume("test.pdf")
    
    def test_parse_resume_with_pdf_parser(self, tmp_path):
        """Test parse_resume with actual PDFParser (mocked)."""
        file_path = tmp_path / "resume.pdf"
        file_path.write_bytes(b"content")
        
        with patch('src.parsers.pdf_parser.pypdf.PdfReader') as mock_reader:
            mock_page = Mock()
            mock_page.extract_text.return_value = "Resume content"
            mock_reader.return_value.pages = [mock_page]
            
            pdf_parser = PDFParser()
            
            mock_llm = Mock()
            mock_name_extractor = Mock()
            mock_name_extractor.extract.return_value = "John Doe"
            mock_email_extractor = Mock()
            mock_email_extractor.extract.return_value = "john@example.com"
            mock_skills_extractor = Mock()
            mock_skills_extractor.extract.return_value = ["Python"]
            
            extractors = {
                'name': mock_name_extractor,
                'email': mock_email_extractor,
                'skills': mock_skills_extractor
            }
            
            resume_extractor = ResumeExtractor(extractors, mock_llm)
            framework = ResumeParserFramework(pdf_parser, resume_extractor)
            
            result = framework.parse_resume(str(file_path))
            
            assert isinstance(result, ResumeData)
            assert result.name == "John Doe"
    
    def test_parse_resume_with_word_parser(self, tmp_path):
        """Test parse_resume with actual WordParser (mocked)."""
        file_path = tmp_path / "resume.docx"
        file_path.write_bytes(b"content")
        
        with patch('src.parsers.word_parser.Document') as mock_document:
            mock_doc = Mock()
            mock_doc.paragraphs = [Mock(text="Resume content")]
            mock_doc.tables = []
            mock_document.return_value = mock_doc
            
            word_parser = WordParser()
            
            mock_llm = Mock()
            mock_name_extractor = Mock()
            mock_name_extractor.extract.return_value = "Jane Smith"
            mock_email_extractor = Mock()
            mock_email_extractor.extract.return_value = "jane@example.com"
            mock_skills_extractor = Mock()
            mock_skills_extractor.extract.return_value = ["Java"]
            
            extractors = {
                'name': mock_name_extractor,
                'email': mock_email_extractor,
                'skills': mock_skills_extractor
            }
            
            resume_extractor = ResumeExtractor(extractors, mock_llm)
            framework = ResumeParserFramework(word_parser, resume_extractor)
            
            result = framework.parse_resume(str(file_path))
            
            assert isinstance(result, ResumeData)
            assert result.name == "Jane Smith"
    
    def test_parse_resume_path_conversion(self):
        """Test parse_resume converts string path to Path object."""
        mock_parser = Mock()
        mock_parser.parse.return_value = "Resume text"
        
        mock_extractor = Mock()
        mock_extractor.extract.return_value = ResumeData(
            name="Test",
            email="test@example.com",
            skills=[]
        )
        
        framework = ResumeParserFramework(mock_parser, mock_extractor)
        
        framework.parse_resume("test.pdf")
        
        # Verify parse was called with Path object
        call_args = mock_parser.parse.call_args[0]
        assert isinstance(call_args[0], Path)
        assert str(call_args[0]) == "test.pdf"

