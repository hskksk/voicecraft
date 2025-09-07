"""
OpenAI Speech Synthesizer Module

This module provides the OpenAI-based speech synthesizer implementation.
"""

from typing import Dict, Any
import litellm
import base64
from .base import SpeechSynthesizer


class OpenAISpeechSynthesizer(SpeechSynthesizer):
    """OpenAI-based speech synthesizer"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.model = config.get('model', 'openai/gpt-4o-audio-preview')
        self.voice = config.get('voice', 'alloy')
        self.response_format = config.get('response_format', 'wav')
    
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
