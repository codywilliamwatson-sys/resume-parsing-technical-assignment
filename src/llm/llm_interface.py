"""Abstract base class for LLM interfaces."""

from abc import ABC, abstractmethod


class LLMInterface(ABC):
    """Abstract base class for interacting with Large Language Models (LLMs)."""
    
    @abstractmethod
    def generate_response(self, prompt: str, **kwargs) -> str:
        """
        Generate a response from the LLM based on the given prompt.
        
        Args:
            prompt: The input prompt/question to send to the LLM
            **kwargs: Additional parameters specific to the LLM implementation
                     (e.g., temperature, max_tokens, etc.)
        
        Returns:
            The generated response text from the LLM
            
        Raises:
            ValueError: If the prompt is invalid
            ConnectionError: If there's an error connecting to the LLM service
            RuntimeError: If there's an error during LLM processing
        """
        pass  # pragma: no cover
    
    def validate_prompt(self, prompt: str) -> None:
        """Validate that the prompt is valid for LLM processing."""
        if prompt is None:
            raise ValueError("Prompt cannot be None")
        
        if not isinstance(prompt, str):
            raise ValueError(f"Prompt must be a string, got {type(prompt).__name__}")
        
        if not prompt.strip():
            raise ValueError("Prompt cannot be empty or whitespace only")
    
    def validate_text(self, text: str) -> None:
        """Validate that the input text is valid for processing."""
        if text is None:
            raise ValueError("Text cannot be None")
        
        if not isinstance(text, str):
            raise ValueError(f"Text must be a string, got {type(text).__name__}")
        
        if not text.strip():
            raise ValueError("Text cannot be empty or whitespace only")

