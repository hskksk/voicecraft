"""
OpenAI Model Information

This module defines the available OpenAI models and their capabilities.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class ModelInfo:
    """Information about an OpenAI model"""
    name: str
    provider: str
    type: str
    description: str
    supported_voices: List[str]
    supported_formats: List[str]
    multi_speaker: bool
    max_text_length: Optional[int] = None
    features: List[str] = None


# OpenAI model definitions
OPENAI_MODELS = {
    "openai/gpt-4o-audio-preview": ModelInfo(
        name="openai/gpt-4o-audio-preview",
        provider="openai",
        type="tts",
        description="OpenAI GPT-4o Audio Preview for text-to-speech",
        supported_voices=[],  # Will be populated from voices.py
        supported_formats=["wav", "pcm16"],
        multi_speaker=False,
        max_text_length=5000,
        features=["high_quality", "fast_generation", "custom_instructions"]
    )
}


def get_model_info(model_name: str) -> Optional[ModelInfo]:
    """Get model information by name"""
    return OPENAI_MODELS.get(model_name)


def list_available_models() -> Dict[str, ModelInfo]:
    """Get all available OpenAI models"""
    return OPENAI_MODELS.copy()


def get_models_by_capability(capability: str) -> List[str]:
    """Get model names that support a specific capability"""
    models = []
    for name, info in OPENAI_MODELS.items():
        if capability == "multi_speaker" and info.multi_speaker:
            models.append(name)
        elif info.features and capability in info.features:
            models.append(name)
    return models


def validate_model(model_name: str) -> bool:
    """Validate if a model name is supported"""
    return model_name in OPENAI_MODELS


def get_supported_formats(model_name: str) -> List[str]:
    """Get supported audio formats for a model"""
    model_info = get_model_info(model_name)
    return model_info.supported_formats if model_info else []


def get_max_text_length(model_name: str) -> Optional[int]:
    """Get maximum text length for a model"""
    model_info = get_model_info(model_name)
    return model_info.max_text_length if model_info else None
