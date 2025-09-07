"""
Speech Synthesizer Package

This package provides speech synthesis functionality with support for multiple
providers including OpenAI and Gemini.
"""

from .base import SpeechSynthesizer
from .openai_synthesizer import OpenAISpeechSynthesizer
from .gemini_synthesizer import GeminiSpeechSynthesizer
from .factory import synthesizer_factory
from .gemini_voices import GEMINI_VOICES, validate_voice, get_voice_info, list_all_voices

__all__ = [
    'SpeechSynthesizer',
    'OpenAISpeechSynthesizer', 
    'GeminiSpeechSynthesizer',
    'synthesizer_factory',
    'GEMINI_VOICES',
    'validate_voice',
    'get_voice_info',
    'list_all_voices'
]
