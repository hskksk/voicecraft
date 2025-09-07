"""
Gemini Speech Synthesizer Module

This module provides the Gemini-based speech synthesizer implementation using
the official Google GenAI SDK with support for multi-speaker functionality.
"""

from typing import Dict, Any, List, Optional
import os
from google import genai
from google.genai import types
from .base import SpeechSynthesizer
from .gemini_voices import GEMINI_VOICES, validate_voice, get_voice_info


class GeminiSpeechSynthesizer(SpeechSynthesizer):
    """Gemini-based speech synthesizer with multi-speaker support"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.model = config.get('model', 'gemini-2.5-flash-preview-tts')
        self.voice = config.get('voice', 'Kore')
        self.response_format = config.get('response_format', 'wav')
        self.multi_speaker = config.get('multi_speaker', False)
        self.speakers = config.get('speakers', [])
        
        # Validate voice names
        self._validate_voices()
        
        # Initialize Gemini client
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable is required")
        self.client = genai.Client(api_key=api_key)
    
    def _validate_voices(self):
        """Validate that all voice names are supported"""
        # Validate single voice
        if not validate_voice(self.voice):
            available_voices = list(GEMINI_VOICES.keys())
            raise ValueError(f"Unsupported voice '{self.voice}'. Available voices: {available_voices}")
        
        # Validate multi-speaker voices
        if self.multi_speaker and self.speakers:
            for speaker in self.speakers:
                if isinstance(speaker, dict):
                    voice_name = speaker.get('voice_name', '')
                else:
                    voice_name = getattr(speaker, 'voice_name', '')
                
                if not validate_voice(voice_name):
                    available_voices = list(GEMINI_VOICES.keys())
                    raise ValueError(f"Unsupported voice '{voice_name}' for speaker. Available voices: {available_voices}")
    
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
            for name, info in GEMINI_VOICES.items()
        }
    
    def _build_prompt(self, text: str, instructions: str = "") -> str:
        """Build the complete prompt including speaker descriptions"""
        prompt_parts = []
        
        # 基本の指示を追加
        if instructions:
            prompt_parts.append(instructions)
        
        # 複数話者モードの場合、話者の説明を追加
        if self.multi_speaker and self.speakers:
            speaker_instructions = self._build_speaker_instructions()
            if speaker_instructions:
                prompt_parts.append(speaker_instructions)
        
        # テキストを追加
        prompt_parts.append(text)
        
        return "\n\n".join(prompt_parts)
    
    def _build_speaker_instructions(self) -> str:
        """Build speaker-specific voice style instructions"""
        if not self.speakers:
            return ""
        
        instructions = []
        instructions.append("Voice style instructions for each speaker:")
        
        for speaker in self.speakers:
            if isinstance(speaker, dict):
                name = speaker.get('name', '')
                description = speaker.get('description', '')
                voice_name = speaker.get('voice_name', '')
            else:
                name = getattr(speaker, 'name', '')
                description = getattr(speaker, 'description', '')
                voice_name = getattr(speaker, 'voice_name', '')
            
            if name and description:
                # 音声の特徴情報も取得
                voice_info = get_voice_info(voice_name)
                voice_characteristic = voice_info.characteristic if voice_info else ""
                
                speaker_instruction = f"- {name}: {description}"
                if voice_characteristic:
                    speaker_instruction += f" (Voice characteristic: {voice_characteristic})"
                
                instructions.append(speaker_instruction)
        
        return "\n".join(instructions)
    
    def synthesize(self, text: str, instructions: str = "") -> bytes:
        """Synthesize speech using Gemini models with optional multi-speaker support"""
        try:
            # プロンプトを構築
            prompt = self._build_prompt(text, instructions)
            
            # 音声設定を構築
            if self.multi_speaker and self.speakers:
                # 複数話者モード
                speech_config = types.SpeechConfig(
                    multi_speaker_voice_config = types.MultiSpeakerVoiceConfig(
                        speaker_voice_configs = [
                            types.SpeakerVoiceConfig(
                                speaker=speaker['name'],
                                voice_config=types.VoiceConfig(
                                    prebuilt_voice_config=types.PrebuiltVoiceConfig(
                                        voice_name=speaker['voice_name']
                                    )
                                )
                            )
                            for speaker in self.speakers
                        ]
                    )
                )
            else:
                # 単一話者モード
                speech_config = types.SpeechConfig(
                    voice_config = types.VoiceConfig(
                        prebuilt_voice_config=types.PrebuiltVoiceConfig(
                            voice_name=self.voice
                        )
                    )
                )
            
            # Gemini APIを使用して音声生成
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_modalities=["AUDIO"],
                    speech_config=speech_config
                )
            )
            
            # 音声データを取得
            audio_data = response.candidates[0].content.parts[0].inline_data.data
            return audio_data
            
        except Exception as e:
            raise RuntimeError(f"Error generating speech with Gemini: {e}")
    
    def add_speaker(self, speaker_name: str, voice_name: str, description: str = ""):
        """Add a speaker for multi-speaker mode"""
        speaker = types.Speaker(
            name=speaker_name,
            voice_name=voice_name,
            description=description
        )
        self.speakers.append(speaker)
        self.multi_speaker = True
    
    def set_speakers(self, speakers: List[Dict[str, str]]):
        """Set multiple speakers for multi-speaker mode
        
        Args:
            speakers: List of speaker dictionaries with 'name', 'voice_name', and optional 'description'
        """
        self.speakers = []
        for speaker_info in speakers:
            speaker = types.Speaker(
                name=speaker_info['name'],
                voice_name=speaker_info['voice_name'],
                description=speaker_info.get('description', '')
            )
            self.speakers.append(speaker)
        self.multi_speaker = len(self.speakers) > 0
