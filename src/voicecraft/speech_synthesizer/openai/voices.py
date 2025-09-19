"""
OpenAI Voice Types and Characteristics

This module defines the available voice types and their characteristics
for OpenAI TTS models.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class VoiceInfo:
    """Information about an OpenAI voice"""
    name: str
    characteristic: str
    category: str  # e.g., "female", "male", "neutral"


# OpenAI voice types and their characteristics
OPENAI_VOICES = {
    "alloy": VoiceInfo("alloy", "Neutral", "neutral"),
    "echo": VoiceInfo("echo", "Clear", "male"),
    "fable": VoiceInfo("fable", "Warm", "male"),
    "onyx": VoiceInfo("onyx", "Deep", "male"),
    "nova": VoiceInfo("nova", "Bright", "female"),
    "shimmer": VoiceInfo("shimmer", "Soft", "female"),
}


def get_voice_info(voice_name: str) -> Optional[VoiceInfo]:
    """Get voice information by name"""
    return OPENAI_VOICES.get(voice_name)


def get_voices_by_characteristic(characteristic: str) -> List[str]:
    """Get voice names that match a specific characteristic"""
    return [
        name for name, info in OPENAI_VOICES.items()
        if characteristic.lower() in info.characteristic.lower()
    ]


def get_voices_by_category(category: str) -> List[str]:
    """Get voice names by category (female, male, neutral)"""
    return [
        name for name, info in OPENAI_VOICES.items()
        if info.category.lower() == category.lower()
    ]


def list_all_voices() -> Dict[str, VoiceInfo]:
    """Get all available voices"""
    return OPENAI_VOICES.copy()


def validate_voice(voice_name: str) -> bool:
    """Validate if a voice name is supported"""
    return voice_name in OPENAI_VOICES


def get_voice_suggestions(text_context: str = "") -> List[str]:
    """Get voice suggestions based on text context"""
    suggestions = []
    
    # Simple keyword-based suggestions
    text_lower = text_context.lower()
    
    if any(word in text_lower for word in ["friendly", "warm", "casual"]):
        suggestions.extend(["fable", "shimmer"])
    
    if any(word in text_lower for word in ["professional", "formal", "business"]):
        suggestions.extend(["alloy", "echo", "onyx"])
    
    if any(word in text_lower for word in ["energetic", "exciting", "dynamic"]):
        suggestions.extend(["nova", "echo"])
    
    if any(word in text_lower for word in ["calm", "gentle", "soft"]):
        suggestions.extend(["shimmer", "alloy"])
    
    # Remove duplicates and return
    return list(set(suggestions))
