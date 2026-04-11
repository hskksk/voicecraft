"""
MCP (Model Context Protocol) API router
"""

import logging
import os
from fastmcp.utilities.types import Audio
import yaml
import base64
import tempfile
import datetime
import hashlib
from pathlib import Path
from typing import Dict, Any, Optional, Annotated, List
from pydantic import Field
from fastapi import FastAPI, HTTPException
from fastmcp import FastMCP
from ..models.responses import (
    SynthesisResponse,
    ErrorResponse,
    ListAvailableModelsResponse,
    ListAvailableVoicesResponse,
    ListAvailableProvidersResponse,
    GenerateConfigResponse,
)
from ..models.requests import (
    ListAvailableVoicesRequest,
    GenerateConfigRequest,
    SynthesizeRequest,
)
from ..dependencies import get_logger
from ...speech_synthesizer import list_synthesizers, synthesizer_factory
from ...filename_generator import FilenameGenerator

logger = logging.getLogger("voicecraft.api.mcp")

def create_mcp_app(parent_app: Optional[FastAPI] = None) -> FastMCP:
    """Create an MCP app"""
    if parent_app:
        """Create an MCP app from a parent app"""
        app = FastMCP.from_fastapi(app=parent_app, name="VoiceCraft MCP")
    else:
        app = FastMCP(name="VoiceCraft MCP")

    @app.tool()
    def generate_config(request: GenerateConfigRequest) -> GenerateConfigResponse:
        """
        Generate a YAML configuration using the ConfigGenerator LLM flow.
        """
        try:
            from ...config_generator import ConfigGenerator

            generator = ConfigGenerator(
                model_name=request.model,
                temperature=request.temperature,
                max_output_tokens=request.max_tokens,
            )

            yaml_text = generator.generate_config(
                user_instructions=request.instructions
            )
            return GenerateConfigResponse(
                success=True,
                message="Configuration generated successfully",
                config_content=yaml_text,
            )
        except Exception as e:
            logger.error(f"MCP generate_config error: {e}")
            return GenerateConfigResponse(
                success=False,
                message=f"Generation failed: {e}",
                config_content=None,
            )

    @app.tool()
    def synthesize(request: SynthesizeRequest) -> SynthesisResponse:
        """
        Advanced speech synthesis with full configuration options using VoiceCraft synthesizers
        """
        try:
            logger.info(f"MCP synthesis request: text='{request.text[:50]}...', model='{request.model}', voice='{request.voice}'")
            
            # Determine model and voice with defaults
            model = request.model or "openai/gpt-4o-audio-preview"
            voice = request.voice or "alloy"
            
            # Build synthesizer configuration
            synthesizer_config = {
                'model': model,
                'voice': voice,
                'response_format': 'wav',
            }
            
            # Add any additional config from request
            if request.config:
                synthesizer_config.update(request.config)
            
            # Create synthesizer instance
            synthesizer = synthesizer_factory(model, synthesizer_config)
            
            # Generate speech
            audio_data = synthesizer.synthesize(request.text, request.instructions)
            
            return SynthesisResponse(
                success=True,
                message="Speech synthesis completed successfully",
                audio_data=Audio(
                    data=audio_data,
                    format="wav",
                    annotations=None,
                ).to_audio_content(),
                model_used=model,
                voice_used=voice,
                config=synthesizer_config
            )
            
        except Exception as e:
            logger.error(f"MCP synthesis error: {e}")
            return SynthesisResponse(
                success=False,
                message=f"Synthesis failed: {str(e)}",
                audio_data=None,
                model_used=request.model,
                voice_used=request.voice,
                config=request.config
            )

    @app.tool()
    def list_available_models() -> ListAvailableModelsResponse:
        """
        List all available speech synthesis models supported by VoiceCraft
        
        Returns:
            Dict containing:
            - models: List[Dict] with model information
            - providers: List[str] of supported providers
        """
        logger.info("Listing available VoiceCraft models")
        
        try:
            synthesizers = list_synthesizers()
            models = []
            for synthesizer in synthesizers.values():
                available_models = synthesizer.get_available_models()
                for model_name, model_info in available_models.items():
                    models.append({
                        "name": model_name,
                        "provider": model_info["provider"],
                        "type": model_info["type"],
                        "description": model_info["description"],
                        "supported_voices": list(synthesizer.get_available_voices().keys()),
                        "supported_formats": model_info["supported_formats"],
                        "multi_speaker": model_info["multi_speaker"],
                        "max_text_length": model_info["max_text_length"],
                        "features": model_info["features"],
                    })

            providers = list(synthesizers.keys())

            return ListAvailableModelsResponse(
                success=True,
                message="Models listed successfully",
                models=models,
                providers=providers,
                total_models=len(models),
            )

        except Exception as e:
            logger.error(f"Error listing available models: {e}")
            return ListAvailableModelsResponse(
                success=False,
                message=f"Error listing available models: {e}",
                models=[],
                providers=[],
                total_models=0,
            )

    @app.tool()
    def list_available_providers() -> ListAvailableProvidersResponse:
        """
        List all available TTS providers supported by VoiceCraft
        
        Returns:
            Dict containing:
            - providers: List[Dict] with provider information
            - total_providers: Number of available providers
        """
        logger.info("Listing available TTS providers")
        
        try:
            synthesizers = list_synthesizers()
            providers = []

            for provider_name, synthesizer_class in synthesizers.items():
                provider_info = {
                    "name": provider_name,
                    "display_name": provider_name.title(),
                    "description": f"{provider_name.title()} speech synthesis provider",
                    "class_name": synthesizer_class.__name__,
                    "module": synthesizer_class.__module__,
                }

                try:
                    available_models = synthesizer_class.get_available_models()
                    provider_info["supported_models"] = list(available_models.keys())
                    provider_info["model_count"] = len(available_models)

                    available_voices = synthesizer_class.get_available_voices()
                    provider_info["supported_voices"] = list(available_voices.keys())
                    provider_info["voice_count"] = len(available_voices)

                    characteristics = list(
                        set(voice_info["characteristic"] for voice_info in available_voices.values())
                    )
                    provider_info["voice_characteristics"] = characteristics

                except Exception as e:
                    logger.warning(
                        f"Could not get detailed info for provider {provider_name}: {e}"
                    )
                    provider_info["supported_models"] = []
                    provider_info["model_count"] = 0
                    provider_info["supported_voices"] = []
                    provider_info["voice_count"] = 0
                    provider_info["voice_characteristics"] = []

                providers.append(provider_info)

            return ListAvailableProvidersResponse(
                success=True,
                message="Providers listed successfully",
                providers=providers,
                total_providers=len(providers),
            )

        except Exception as e:
            logger.error(f"Error listing available providers: {e}")
            return ListAvailableProvidersResponse(
                success=False,
                message=f"Error listing available providers: {e}",
                providers=[],
                total_providers=0,
            )

    @app.tool()
    def list_available_voices(
        request: ListAvailableVoicesRequest,
    ) -> ListAvailableVoicesResponse:
        """
        List available voices for speech synthesis
        
        Args:
            provider: Filter by provider name (openai, gemini)
            characteristic: Filter by voice characteristic (e.g., "Bright", "Firm", "Friendly")
        
        Returns:
            Dict containing:
            - voices: List[Dict] with voice information
            - characteristics: List[str] of available characteristics
        """
        logger.info(f"Listing available voices for provider: {request.provider}, characteristic: {request.characteristic}")
        
        try:
            synthesizers = list_synthesizers()
            voices = []

            for provider_name, synthesizer in synthesizers.items():
                voices_data = synthesizer.get_available_voices()

                for voice_name, voice_info in voices_data.items():
                    voices.append(
                        {
                            "name": voice_name,
                            "characteristic": voice_info["characteristic"],
                            "category": voice_info["category"],
                            "provider": provider_name,
                        }
                    )

            if request.provider:
                voices = [v for v in voices if v["provider"] == request.provider]

            if request.characteristic:
                characteristic_filter = request.characteristic.lower()
                voices = [
                    voice
                    for voice in voices
                    if characteristic_filter in voice["characteristic"].lower()
                ]

            characteristics = list(set(voice["characteristic"] for voice in voices))
            characteristics.sort()

            providers = list(set(voice["provider"] for voice in voices))
            providers.sort()

            return ListAvailableVoicesResponse(
                success=True,
                message="Voices listed successfully",
                voices=voices,
                characteristics=characteristics,
                total_voices=len(voices),
                providers=providers,
            )

        except Exception as e:
            logger.error(f"Error listing available voices: {e}")
            return ListAvailableVoicesResponse(
                success=False,
                message=f"Error listing available voices: {e}",
                voices=[],
                characteristics=[],
                providers=[],
                total_voices=0,
            )

    return app