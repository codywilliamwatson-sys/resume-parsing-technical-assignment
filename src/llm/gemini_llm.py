"""
Google Gemini LLM interface implementation.
Handles interaction with Google's Gemini API.
"""

import os
from typing import Optional
import google.genai as genai

from .llm_interface import LLMInterface


class GeminiLLM(LLMInterface):
    """Implementation of LLMInterface for Google Gemini."""
    
    def __init__(self, model_name: str = "models/gemini-2.0-flash-lite", api_key: Optional[str] = None):
        """
        Initialize the Gemini LLM interface.
        
        Args:
            model_name: Name of the Gemini model to use (default: "models/gemini-2.0-flash-lite")
            api_key: Optional API key. If not provided, will be loaded from 
                    GEMINI_API_KEY environment variable
        
        Raises:
            ValueError: If API key is not provided and not found in environment variables
        """
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        
        if not self.api_key:
            raise ValueError(
                "Gemini API key is not set. Please provide it as a parameter "
                "or set the GEMINI_API_KEY environment variable."
            )
        
        self.client = genai.Client(api_key=self.api_key)
        self.model_name = model_name
    
    def generate_response(self, prompt: str, **kwargs) -> str:
        """
        Generate a response from Gemini based on the given prompt.
        
        Args:
            prompt: The input prompt/question to send to Gemini
            **kwargs: Additional parameters:
                - temperature: Controls randomness (0.0 to 1.0)
                - max_output_tokens: Maximum number of tokens in the response
                - top_p: Nucleus sampling parameter
                - top_k: Top-k sampling parameter
        
        Returns:
            The generated response text from Gemini
            
        Raises:
            ValueError: If the prompt is invalid
            ConnectionError: If there's an error connecting to Gemini API
            RuntimeError: If there's an error during Gemini processing
        """
        self.validate_prompt(prompt)
        
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config={
                    'temperature': kwargs.get('temperature', 0.7),
                    'max_output_tokens': kwargs.get('max_output_tokens', 2048),
                    'top_p': kwargs.get('top_p', 0.8),
                    'top_k': kwargs.get('top_k', 40),
                }
            )
            
            return response.text
            
        except Exception as e:
            error_msg = str(e).lower()
            if 'api_key' in error_msg or 'api key' in error_msg or 'authentication' in error_msg or 'invalid' in error_msg and 'key' in error_msg:
                raise ConnectionError(f"Failed to authenticate with Gemini API: {str(e)}") from e
            elif 'network' in error_msg or 'connection' in error_msg:
                raise ConnectionError(f"Failed to connect to Gemini API: {str(e)}") from e
            else:
                raise RuntimeError(f"Error generating response from Gemini: {str(e)}") from e

