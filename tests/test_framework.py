"""Tests for ResumeParserFramework."""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch

from src.framework.resume_parser_framework import ResumeParserFramework
from src.parsers.pdf_parser import PDFParser
from src.parsers.word_parser import WordParser
from src.extractors.resume_extractor import ResumeExtractor
from src.models.resume import ResumeData


class TestResumeParserFramework:
    """Test cases for ResumeParserFramework."""
    
    def test_init_with_default_parsers(self):
        """Test ResumeParserFramework initialization with default parsers."""
        mock_extractor = Mock()
        
        framework = ResumeParserFramework(mock_extractor)
        
        assert len(framework.parsers) == 2
        assert isinstance(framework.parsers[0], PDFParser)
        assert isinstance(framework.parsers[1], WordParser)
        assert framework.resume_extractor == mock_extractor
    
    def test_init_with_custom_parsers(self):
        """Test ResumeParserFramework initialization with custom parsers."""
        mock_extractor = Mock()
        custom_parsers = [PDFParser()]
        
        framework = ResumeParserFramework(mock_extractor, parsers=custom_parsers)
        
        assert framework.parsers == custom_parsers
        assert framework.resume_extractor == mock_extractor
    
    def test_init_with_empty_parsers(self):
        """Test ResumeParserFramework raises ValueError with empty parsers list."""
        mock_extractor = Mock()
        
        with pytest.raises(ValueError, match="Parsers list cannot be empty"):
            ResumeParserFramework(mock_extractor, parsers=[])
    
    def test_parse_resume_success(self, tmp_path):
        """Test successful resume parsing with automatic parser selection."""
        # Setup
        file_path = tmp_path / "resume.pdf"
        file_path.write_bytes(b"fake pdf content")
        
        mock_parser = Mock(spec=PDFParser)
        mock_parser.parse.return_value = "Resume text content"
        mock_parser.can_parse.return_value = True
        mock_parser.get_supported_extensions.return_value = ['.pdf']
        
        mock_llm = Mock()
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
        
        framework = ResumeParserFramework(resume_extractor, parsers=[mock_parser])
        
        # Execute
        result = framework.parse_resume(str(file_path))
        
        # Assert
        assert isinstance(result, ResumeData)
        assert result.name == "John Doe"
        assert result.email == "john.doe@example.com"
        assert result.skills == ["Python", "Java"]
        mock_parser.parse.assert_called_once_with(Path(file_path))
        mock_parser.can_parse.assert_called_once_with(Path(file_path))
    
    def test_parse_resume_file_not_found(self):
        """Test parse_resume raises FileNotFoundError for non-existent file."""
        mock_parser = Mock(spec=PDFParser)
        mock_parser.can_parse.return_value = True
        mock_parser.parse.side_effect = FileNotFoundError("File not found")
        
        mock_extractor = Mock()
        
        framework = ResumeParserFramework(mock_extractor, parsers=[mock_parser])
        
        with pytest.raises(FileNotFoundError):
            framework.parse_resume("nonexistent.pdf")
    
    def test_parse_resume_invalid_format(self):
        """Test parse_resume raises ValueError for invalid file format."""
        mock_parser = Mock(spec=PDFParser)
        mock_parser.can_parse.return_value = True
        mock_parser.parse.side_effect = ValueError("Invalid file format")
        
        mock_extractor = Mock()
        
        framework = ResumeParserFramework(mock_extractor, parsers=[mock_parser])
        
        with pytest.raises(ValueError):
            framework.parse_resume("invalid.pdf")
    
    def test_parse_resume_unsupported_extension(self):
        """Test parse_resume raises ValueError for unsupported file extension."""
        mock_extractor = Mock()
        
        framework = ResumeParserFramework(mock_extractor)
        
        with pytest.raises(ValueError, match="No parser available for file extension"):
            framework.parse_resume("file.xyz")
    
    def test_parse_resume_io_error(self):
        """Test parse_resume raises IOError for file read errors."""
        mock_parser = Mock(spec=PDFParser)
        mock_parser.can_parse.return_value = True
        mock_parser.parse.side_effect = IOError("Cannot read file")
        
        mock_extractor = Mock()
        
        framework = ResumeParserFramework(mock_extractor, parsers=[mock_parser])
        
        with pytest.raises(IOError):
            framework.parse_resume("test.pdf")
    
    def test_parse_resume_extraction_failure(self):
        """Test parse_resume handles extraction failures."""
        mock_parser = Mock(spec=PDFParser)
        mock_parser.can_parse.return_value = True
        mock_parser.parse.return_value = "Resume text"
        
        mock_extractor = Mock()
        mock_extractor.extract.side_effect = ValueError("Extraction failed")
        
        framework = ResumeParserFramework(mock_extractor, parsers=[mock_parser])
        
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
            framework = ResumeParserFramework(resume_extractor)
            
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
            framework = ResumeParserFramework(resume_extractor)
            
            result = framework.parse_resume(str(file_path))
            
            assert isinstance(result, ResumeData)
            assert result.name == "Jane Smith"
    
    def test_parse_resume_path_conversion(self):
        """Test parse_resume converts string path to Path object."""
        mock_parser = Mock(spec=PDFParser)
        mock_parser.can_parse.return_value = True
        mock_parser.parse.return_value = "Resume text"
        
        mock_extractor = Mock()
        mock_extractor.extract.return_value = ResumeData(
            name="Test",
            email="test@example.com",
            skills=[]
        )
        
        framework = ResumeParserFramework(mock_extractor, parsers=[mock_parser])
        
        framework.parse_resume("test.pdf")
        
        # Verify parse was called with Path object
        call_args = mock_parser.parse.call_args[0]
        assert isinstance(call_args[0], Path)
        assert str(call_args[0]) == "test.pdf"
    
    def test_select_parser_for_pdf(self):
        """Test parser selection for PDF files."""
        mock_extractor = Mock()
        framework = ResumeParserFramework(mock_extractor)
        
        pdf_path = Path("test.pdf")
        selected_parser = framework._select_parser(pdf_path)
        
        assert isinstance(selected_parser, PDFParser)
    
    def test_select_parser_for_word(self):
        """Test parser selection for Word files."""
        mock_extractor = Mock()
        framework = ResumeParserFramework(mock_extractor)
        
        word_path = Path("test.docx")
        selected_parser = framework._select_parser(word_path)
        
        assert isinstance(selected_parser, WordParser)

