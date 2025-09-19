"""
OpenAI Speech Synthesizer Module

This module provides the OpenAI-based speech synthesizer implementation.
"""

from typing import Dict, Any, Optional
import litellm
import base64
from ..base import SpeechSynthesizer
from .voices import OPENAI_VOICES, validate_voice, get_voice_info
from .models import get_model_info, validate_model, list_available_models


class OpenAISpeechSynthesizer(SpeechSynthesizer):
    """OpenAI-based speech synthesizer"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.model = config.get('model', 'openai/gpt-4o-audio-preview')
        self.voice = config.get('voice', 'alloy')
        self.response_format = config.get('response_format', 'wav')
        
        # Validate model and voice names
        self._validate_model()
        self._validate_voice()
    
    def _validate_model(self):
        """Validate that the model is supported"""
        if not validate_model(self.model):
            available_models = list(get_model_info(self.model).keys()) if get_model_info(self.model) else []
            raise ValueError(f"Unsupported model '{self.model}'. Available models: {available_models}")
    
    def _validate_voice(self):
        """Validate that the voice is supported"""
        if not validate_voice(self.voice):
            available_voices = list(OPENAI_VOICES.keys())
            raise ValueError(f"Unsupported voice '{self.voice}'. Available voices: {available_voices}")
    
    def get_voice_info(self, voice_name: str = None) -> Optional[Dict[str, str]]:
        """Get information about a voice"""
        if voice_name is None:
            voice_name = self.voice
        
        voice_info = get_voice_info(voice_name)
        if voice_info:
            return {
                'name': voice_info.name,
                'characteristic': voice_info.characteristic,
                'category': voice_info.category
            }
        return None
    
    def list_available_voices(self) -> Dict[str, Dict[str, str]]:
        """List all available voices with their characteristics"""
        return {
            name: {
                'characteristic': info.characteristic,
                'category': info.category
            }
            for name, info in OPENAI_VOICES.items()
        }
    
    def synthesize(self, text: str, instructions: str = "") -> bytes:
        """Synthesize speech using OpenAI models"""
        try:
            # プロンプトを構築
            prompt = text
            if instructions:
                prompt = f"{instructions}\n\n{text}"
            
            # LiteLLMを使用して音声生成
            completion = litellm.completion(
                model=self.model,
                modalities=["text", "audio"],
                audio={"voice": self.voice, "format": self.response_format},
                messages=[{"role": "user", "content": prompt}],
            )
            
            # 音声データを取得（base64デコード）
            audio_data_b64 = completion.choices[0].message.audio.data
            audio_data = base64.b64decode(audio_data_b64)
            return audio_data
            
        except Exception as e:
            raise RuntimeError(f"Error generating speech with OpenAI: {e}")
    
    @classmethod
    def get_available_voices(cls) -> Dict[str, Dict[str, str]]:
        """
        Get available voices for OpenAI synthesizer
        
        Returns:
            Dictionary mapping voice names to their characteristics
        """
        return {
            name: {
                'characteristic': info.characteristic,
                'category': info.category
            }
            for name, info in OPENAI_VOICES.items()
        }
    
    @classmethod
    def get_available_models(cls) -> Dict[str, Dict[str, Any]]:
        """
        Get available models for OpenAI synthesizer
        
        Returns:
            Dictionary mapping model names to their information
        """
        models = {}
        for model_name, model_info in list_available_models().items():
            models[model_name] = {
                'name': model_info.name,
                'provider': model_info.provider,
                'type': model_info.type,
                'description': model_info.description,
                'supported_formats': model_info.supported_formats,
                'multi_speaker': model_info.multi_speaker,
                'max_text_length': model_info.max_text_length,
                'features': model_info.features or []
            }
        return models
