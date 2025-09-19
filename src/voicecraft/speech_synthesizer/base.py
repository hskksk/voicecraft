"""
Base Speech Synthesizer Module

This module provides the abstract base class for speech synthesis.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List


class SpeechSynthesizer(ABC):
    """Abstract base class for speech synthesis"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the speech synthesizer
        
        Args:
            config: Configuration dictionary containing model-specific settings
        """
        self.config = config
    
    @abstractmethod
    def synthesize(self, text: str, instructions: str = "") -> bytes:
        """
        Synthesize speech from text
        
        Args:
            text: Text to convert to speech
            instructions: Additional instructions for speech generation
            
        Returns:
            Audio data as bytes
        """
        pass
    
    @classmethod
    @abstractmethod
    def get_available_voices(cls) -> Dict[str, Dict[str, str]]:
        """
        Get available voices for this synthesizer
        
        Returns:
            Dictionary mapping voice names to their characteristics
        """
        pass
    
    @classmethod
    @abstractmethod
    def get_available_models(cls) -> Dict[str, Dict[str, Any]]:
        """
        Get available models for this synthesizer
        
        Returns:
            Dictionary mapping model names to their information
        """
        pass
