"""
Response models for API endpoints
"""

from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field

class BaseResponse(BaseModel):
    """Base response model"""
    success: bool = Field(..., description="Whether the request was successful")
    message: Optional[str] = Field(None, description="Response message")

class SynthesisResponse(BaseResponse):
    """Synthesis response model"""
    audio_data: Optional[str] = Field(None, description="Base64 encoded audio data")
    audio_format: Optional[str] = Field("wav", description="Audio format")
    duration: Optional[float] = Field(None, description="Audio duration in seconds")
    model_used: Optional[str] = Field(None, description="Model that was used")
    voice_used: Optional[str] = Field(None, description="Voice that was used")


class ListAvailableModelsResponse(BaseResponse):
    """Response model for listing available models"""

    models: List[Dict[str, Any]] = Field(
        default_factory=list,
        description=(
            "List of model information dictionaries. Each item typically includes "
            "name, provider, type, description, supported_voices, supported_formats, "
            "multi_speaker, max_text_length, and features."
        ),
    )
    providers: List[str] = Field(
        default_factory=list,
        description="List of supported provider names.",
    )
    total_models: Optional[int] = Field(
        default=None,
        description="Total number of models available.",
    )


class ListAvailableVoicesResponse(BaseResponse):
    """Response model for listing available voices"""

    voices: List[Dict[str, Any]] = Field(
        default_factory=list,
        description=(
            "List of voice information dictionaries. Each item typically includes "
            "name, characteristic, category, and provider."
        ),
    )
    characteristics: List[str] = Field(
        default_factory=list,
        description="List of unique voice characteristics present in the response.",
    )
    total_voices: Optional[int] = Field(
        default=None,
        description="Total number of voices returned after filtering.",
    )
    providers: List[str] = Field(
        default_factory=list,
        description="List of provider names present in the voices result.",
    )


class ListAvailableProvidersResponse(BaseResponse):
    """Response model for listing available TTS providers"""

    providers: List[Dict[str, Any]] = Field(
        default_factory=list,
        description=(
            "List of provider information dictionaries. Each item typically includes "
            "name, display_name, description, class_name, module, supported_models, "
            "model_count, supported_voices, voice_count, and voice_characteristics."
        ),
    )
    total_providers: Optional[int] = Field(
        default=None,
        description="Total number of providers available.",
    )

class ErrorResponse(BaseResponse):
    """Error response model"""
    error_code: Optional[str] = Field(None, description="Error code")
    details: Optional[Dict[str, Any]] = Field(None, description="Error details")

class HealthResponse(BaseModel):
    """Health check response model"""
    status: str = Field(..., description="Service status")
    service: str = Field(..., description="Service name")
    version: Optional[str] = Field(None, description="Service version")
    timestamp: Optional[str] = Field(None, description="Response timestamp")


class GenerateConfigResponse(BaseResponse):
    """Response model for config generation tool."""
    config_content: Optional[str] = Field(
        default=None, description="Generated YAML configuration content as a string."
    )
