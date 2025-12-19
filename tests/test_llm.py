"""Tests for LLM interfaces."""

import pytest
import os
from unittest.mock import Mock, patch, MagicMock

from src.llm.gemini_llm import GeminiLLM
from src.llm.llm_interface import LLMInterface


class TestLLMInterface:
    """Test cases for LLMInterface abstract class."""
    
    def test_validate_prompt_none(self):
        """Test validate_prompt raises ValueError for None."""
        # Create a concrete implementation for testing
        class TestLLM(LLMInterface):
            def generate_response(self, prompt: str, **kwargs) -> str:
                return ""
        
        llm = TestLLM()
        
        with pytest.raises(ValueError, match="Prompt cannot be None"):
            llm.validate_prompt(None)
    
    def test_validate_prompt_not_string(self):
        """Test validate_prompt raises ValueError for non-string."""
        class TestLLM(LLMInterface):
            def generate_response(self, prompt: str, **kwargs) -> str:
                return ""
        
        llm = TestLLM()
        
        with pytest.raises(ValueError, match="Prompt must be a string"):
            llm.validate_prompt(123)
        
        # Test with different non-string types to ensure full coverage
        with pytest.raises(ValueError, match="Prompt must be a string"):
            llm.validate_prompt([])
        with pytest.raises(ValueError, match="Prompt must be a string"):
            llm.validate_prompt({})
    
    def test_validate_prompt_empty(self):
        """Test validate_prompt raises ValueError for empty string."""
        class TestLLM(LLMInterface):
            def generate_response(self, prompt: str, **kwargs) -> str:
                return ""
        
        llm = TestLLM()
        
        with pytest.raises(ValueError, match="Prompt cannot be empty"):
            llm.validate_prompt("")
        with pytest.raises(ValueError, match="Prompt cannot be empty"):
            llm.validate_prompt("   ")
    
    def test_validate_text_none(self):
        """Test validate_text raises ValueError for None."""
        class TestLLM(LLMInterface):
            def generate_response(self, prompt: str, **kwargs) -> str:
                return ""
        
        llm = TestLLM()
        
        with pytest.raises(ValueError, match="Text cannot be None"):
            llm.validate_text(None)
    
    def test_validate_text_not_string(self):
        """Test validate_text raises ValueError for non-string."""
        class TestLLM(LLMInterface):
            def generate_response(self, prompt: str, **kwargs) -> str:
                return ""
        
        llm = TestLLM()
        
        with pytest.raises(ValueError, match="Text must be a string"):
            llm.validate_text(123)
        
        # Test with different non-string types to ensure full coverage
        with pytest.raises(ValueError, match="Text must be a string"):
            llm.validate_text([])
        with pytest.raises(ValueError, match="Text must be a string"):
            llm.validate_text({})
    
    def test_validate_text_empty(self):
        """Test validate_text raises ValueError for empty string."""
        class TestLLM(LLMInterface):
            def generate_response(self, prompt: str, **kwargs) -> str:
                return ""
        
        llm = TestLLM()
        
        with pytest.raises(ValueError, match="Text cannot be empty"):
            llm.validate_text("")
        with pytest.raises(ValueError, match="Text cannot be empty"):
            llm.validate_text("   ")


class TestGeminiLLM:
    """Test cases for GeminiLLM."""
    
    @patch.dict(os.environ, {'GEMINI_API_KEY': 'test-api-key'})
    @patch('src.llm.gemini_llm.genai')
    def test_init_with_env_var(self, mock_genai):
        """Test GeminiLLM initialization with environment variable."""
        mock_client = Mock()
        mock_genai.Client.return_value = mock_client
        
        llm = GeminiLLM()
        
        assert llm.api_key == 'test-api-key'
        assert llm.model_name == 'models/gemini-2.0-flash-lite'
        mock_genai.Client.assert_called_once_with(api_key='test-api-key')
        assert llm.client == mock_client
    
    @patch('src.llm.gemini_llm.genai')
    def test_init_with_api_key_parameter(self, mock_genai):
        """Test GeminiLLM initialization with API key parameter."""
        mock_client = Mock()
        mock_genai.Client.return_value = mock_client
        
        llm = GeminiLLM(api_key='custom-api-key')
        
        assert llm.api_key == 'custom-api-key'
        mock_genai.Client.assert_called_once_with(api_key='custom-api-key')
    
    @patch('src.llm.gemini_llm.genai')
    def test_init_with_custom_model(self, mock_genai):
        """Test GeminiLLM initialization with custom model name."""
        mock_client = Mock()
        mock_genai.Client.return_value = mock_client
        
        llm = GeminiLLM(model_name='gemini-ultra', api_key='test-key')
        
        assert llm.model_name == 'gemini-ultra'
        mock_genai.Client.assert_called_once_with(api_key='test-key')
    
    @patch.dict(os.environ, {}, clear=True)
    def test_init_no_api_key(self):
        """Test GeminiLLM initialization raises ValueError when no API key provided."""
        with pytest.raises(ValueError, match="Gemini API key is not set"):
            GeminiLLM()
    
    @patch.dict(os.environ, {'GEMINI_API_KEY': 'test-api-key'})
    @patch('src.llm.gemini_llm.genai')
    def test_generate_response_success(self, mock_genai):
        """Test successful response generation."""
        mock_response = Mock()
        mock_response.text = "Generated response"
        
        mock_client = Mock()
        mock_client.models.generate_content.return_value = mock_response
        mock_genai.Client.return_value = mock_client
        
        llm = GeminiLLM()
        result = llm.generate_response("Test prompt")
        
        assert result == "Generated response"
        mock_client.models.generate_content.assert_called_once()
    
    @patch.dict(os.environ, {'GEMINI_API_KEY': 'test-api-key'})
    @patch('src.llm.gemini_llm.genai')
    def test_generate_response_with_kwargs(self, mock_genai):
        """Test response generation with custom parameters."""
        mock_response = Mock()
        mock_response.text = "Generated response"
        
        mock_client = Mock()
        mock_client.models.generate_content.return_value = mock_response
        mock_genai.Client.return_value = mock_client
        
        llm = GeminiLLM()
        result = llm.generate_response(
            "Test prompt",
            temperature=0.5,
            max_output_tokens=1000
        )
        
        assert result == "Generated response"
        call_args = mock_client.models.generate_content.call_args
        assert call_args[1]['config']['temperature'] == 0.5
        assert call_args[1]['config']['max_output_tokens'] == 1000
    
    @patch.dict(os.environ, {'GEMINI_API_KEY': 'test-api-key'})
    @patch('src.llm.gemini_llm.genai')
    def test_generate_response_default_parameters(self, mock_genai):
        """Test response generation uses default parameters."""
        mock_response = Mock()
        mock_response.text = "Generated response"
        
        mock_client = Mock()
        mock_client.models.generate_content.return_value = mock_response
        mock_genai.Client.return_value = mock_client
        
        llm = GeminiLLM()
        llm.generate_response("Test prompt")
        
        call_args = mock_client.models.generate_content.call_args
        config = call_args[1]['config']
        assert config['temperature'] == 0.7
        assert config['max_output_tokens'] == 2048
        assert config['top_p'] == 0.8
        assert config['top_k'] == 40
    
    @patch.dict(os.environ, {'GEMINI_API_KEY': 'test-api-key'})
    @patch('src.llm.gemini_llm.genai')
    def test_generate_response_authentication_error(self, mock_genai):
        """Test generate_response raises ConnectionError for authentication errors."""
        mock_client = Mock()
        mock_client.models.generate_content.side_effect = Exception("Invalid API key")
        mock_genai.Client.return_value = mock_client
        
        llm = GeminiLLM()
        
        with pytest.raises(ConnectionError, match="Failed to authenticate"):
            llm.generate_response("Test prompt")
    
    @patch.dict(os.environ, {'GEMINI_API_KEY': 'test-api-key'})
    @patch('src.llm.gemini_llm.genai')
    def test_generate_response_network_error(self, mock_genai):
        """Test generate_response raises ConnectionError for network errors."""
        mock_client = Mock()
        mock_client.models.generate_content.side_effect = Exception("Network connection failed")
        mock_genai.Client.return_value = mock_client
        
        llm = GeminiLLM()
        
        with pytest.raises(ConnectionError, match="Failed to connect"):
            llm.generate_response("Test prompt")
    
    @patch.dict(os.environ, {'GEMINI_API_KEY': 'test-api-key'})
    @patch('src.llm.gemini_llm.genai')
    def test_generate_response_runtime_error(self, mock_genai):
        """Test generate_response raises RuntimeError for other errors."""
        mock_client = Mock()
        mock_client.models.generate_content.side_effect = Exception("Unknown error")
        mock_genai.Client.return_value = mock_client
        
        llm = GeminiLLM()
        
        with pytest.raises(RuntimeError, match="Error generating response"):
            llm.generate_response("Test prompt")
    
    @patch.dict(os.environ, {'GEMINI_API_KEY': 'test-api-key'})
    @patch('src.llm.gemini_llm.genai')
    def test_generate_response_invalid_prompt(self, mock_genai):
        """Test generate_response raises ValueError for invalid prompt."""
        mock_client = Mock()
        mock_genai.Client.return_value = mock_client
        
        llm = GeminiLLM()
        
        with pytest.raises(ValueError, match="Prompt cannot be empty"):
            llm.generate_response("")

