"""
Speech Synthesizer Package

This package provides speech synthesis functionality with support for multiple
providers including OpenAI and Gemini.
"""

from .base import SpeechSynthesizer
from .factory import synthesizer_factory, list_synthesizers

# Import from provider-specific modules
from .openai import OpenAISpeechSynthesizer, OPENAI_VOICES as OPENAI_VOICES_DATA
from .gemini import GeminiSpeechSynthesizer, GEMINI_VOICES as GEMINI_VOICES_DATA

# For backward compatibility, export the main voice data
GEMINI_VOICES = GEMINI_VOICES_DATA
OPENAI_VOICES = OPENAI_VOICES_DATA

__all__ = [
    'SpeechSynthesizer',
    'OpenAISpeechSynthesizer', 
    'GeminiSpeechSynthesizer',
    'synthesizer_factory',
    'list_synthesizers',
]
