"""
OpenAI Speech Synthesizer Package
"""

from .synthesizer import OpenAISpeechSynthesizer
from .voices import OPENAI_VOICES, get_voice_info, validate_voice, list_all_voices
from .models import OPENAI_MODELS, get_model_info, list_available_models

__all__ = [
    'OpenAISpeechSynthesizer',
    'OPENAI_VOICES',
    'get_voice_info',
    'validate_voice',
    'list_all_voices',
    'OPENAI_MODELS',
    'get_model_info',
    'list_available_models'
]
