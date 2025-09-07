"""
Speech Synthesizer Factory Module

This module provides the factory function to create appropriate speech synthesizer
instances based on model names.
"""

from typing import Dict, Any
from .base import SpeechSynthesizer
from .openai_synthesizer import OpenAISpeechSynthesizer
from .gemini_synthesizer import GeminiSpeechSynthesizer


def synthesizer_factory(model_name: str, config: Dict[str, Any]) -> SpeechSynthesizer:
    """
    Factory function to create appropriate speech synthesizer based on model name
    
    Args:
        model_name: Name of the model (e.g., 'openai/gpt-4o-audio-preview')
        config: Configuration dictionary for the synthesizer
        
    Returns:
        Appropriate SpeechSynthesizer instance
        
    Raises:
        ValueError: If model_name is not supported
    """
    # モデル名に基づいて適切なクラスを選択
    if 'openai' in model_name.lower() or 'gpt' in model_name.lower():
        return OpenAISpeechSynthesizer(config)
    elif 'gemini' in model_name.lower():
        return GeminiSpeechSynthesizer(config)
    else:
        raise ValueError(f"Unsupported model: {model_name}. Supported models: OpenAI (gpt-*) and Gemini (gemini-*)")
