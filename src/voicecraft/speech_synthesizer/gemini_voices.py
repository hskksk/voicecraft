"""
Gemini Voice Types and Characteristics

This module defines the available voice types and their characteristics
for Gemini TTS models.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class VoiceInfo:
    """Information about a Gemini voice"""
    name: str
    characteristic: str
    category: str  # e.g., "female", "male", "neutral"


# Gemini voice types and their characteristics
GEMINI_VOICES = {
    # Bright voices
    "Zephyr": VoiceInfo("Zephyr", "Bright", "neutral"),
    "Autonoe": VoiceInfo("Autonoe", "Bright", "female"),
    
    # Upbeat voices
    "Puck": VoiceInfo("Puck", "Upbeat", "male"),
    "Laomedeia": VoiceInfo("Laomedeia", "アップビート", "female"),
    
    # Informative voices
    "Charon": VoiceInfo("Charon", "情報が豊富", "male"),
    "Rasalgethi": VoiceInfo("Rasalgethi", "情報が豊富", "male"),
    "Sadaltager": VoiceInfo("Sadaltager", "Knowledgeable", "male"),
    
    # Firm voices
    "Kore": VoiceInfo("Kore", "Firm", "female"),
    "Orus": VoiceInfo("Orus", "Firm", "male"),
    "Alnilam": VoiceInfo("Alnilam", "Firm", "male"),
    
    # Excitable voices
    "Fenrir": VoiceInfo("Fenrir", "Excitable", "male"),
    
    # Youthful voices
    "Leda": VoiceInfo("Leda", "Youthful", "female"),
    
    # Breezy voices
    "Aoede": VoiceInfo("Aoede", "Breezy", "female"),
    
    # Relaxed voices
    "Callirrhoe": VoiceInfo("Callirrhoe", "おおらか", "female"),
    "Umbriel": VoiceInfo("Umbriel", "Easy-going", "female"),
    
    # Breathy voices
    "Enceladus": VoiceInfo("Enceladus", "Breathy", "male"),
    
    # Clear voices
    "Iapetus": VoiceInfo("Iapetus", "Clear", "male"),
    "Erinome": VoiceInfo("Erinome", "クリア", "female"),
    
    # Smooth voices
    "Algieba": VoiceInfo("Algieba", "Smooth", "male"),
    "Despina": VoiceInfo("Despina", "Smooth", "female"),
    
    # Gravelly voices
    "Algenib": VoiceInfo("Algenib", "Gravelly", "male"),
    
    # Soft voices
    "Achernar": VoiceInfo("Achernar", "Soft", "male"),
    
    # Even voices
    "Schedar": VoiceInfo("Schedar", "Even", "female"),
    
    # Mature voices
    "Gacrux": VoiceInfo("Gacrux", "成人向け", "male"),
    
    # Forward voices
    "Pulcherrima": VoiceInfo("Pulcherrima", "Forward", "female"),
    
    # Friendly voices
    "Achird": VoiceInfo("Achird", "フレンドリー", "female"),
    
    # Casual voices
    "Zubenelgenubi": VoiceInfo("Zubenelgenubi", "カジュアル", "male"),
    
    # Gentle voices
    "Vindemiatrix": VoiceInfo("Vindemiatrix", "Gentle", "female"),
    
    # Lively voices
    "Sadachbia": VoiceInfo("Sadachbia", "Lively", "female"),
    
    # Warm voices
    "Sulafat": VoiceInfo("Sulafat", "Warm", "female"),
}


def get_voice_info(voice_name: str) -> Optional[VoiceInfo]:
    """Get voice information by name"""
    return GEMINI_VOICES.get(voice_name)


def get_voices_by_characteristic(characteristic: str) -> List[str]:
    """Get voice names that match a specific characteristic"""
    return [
        name for name, info in GEMINI_VOICES.items()
        if characteristic.lower() in info.characteristic.lower()
    ]


def get_voices_by_category(category: str) -> List[str]:
    """Get voice names by category (female, male, neutral)"""
    return [
        name for name, info in GEMINI_VOICES.items()
        if info.category.lower() == category.lower()
    ]


def list_all_voices() -> Dict[str, VoiceInfo]:
    """Get all available voices"""
    return GEMINI_VOICES.copy()


def validate_voice(voice_name: str) -> bool:
    """Validate if a voice name is supported"""
    return voice_name in GEMINI_VOICES


def get_voice_suggestions(text_context: str = "") -> List[str]:
    """Get voice suggestions based on text context"""
    suggestions = []
    
    # Simple keyword-based suggestions
    text_lower = text_context.lower()
    
    if any(word in text_lower for word in ["friendly", "warm", "casual"]):
        suggestions.extend(["Achird", "Sulafat", "Zubenelgenubi"])
    
    if any(word in text_lower for word in ["professional", "formal", "business"]):
        suggestions.extend(["Kore", "Alnilam", "Charon"])
    
    if any(word in text_lower for word in ["energetic", "exciting", "dynamic"]):
        suggestions.extend(["Fenrir", "Laomedeia", "Sadachbia"])
    
    if any(word in text_lower for word in ["calm", "gentle", "soft"]):
        suggestions.extend(["Vindemiatrix", "Achernar", "Callirrhoe"])
    
    # Remove duplicates and return
    return list(set(suggestions))
