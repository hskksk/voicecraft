"""
Base Speech Synthesizer Module

This module provides the abstract base class for speech synthesis.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any


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
