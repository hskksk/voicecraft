from typing import Optional, Dict, Any
from pydantic import BaseModel, Field


class SynthesizeRequest(BaseModel):
    """Request model for speech synthesis."""
    
    text: str = Field(..., description="Text to synthesize into speech")
    model: Optional[str] = Field(
        default=None, 
        description="Model name for synthesis (e.g., 'openai/gpt-4o-audio-preview', 'gemini-2.5-flash-preview-tts')"
    )
    voice: Optional[str] = Field(
        default=None, 
        description="Voice name for synthesis (e.g., 'alloy', 'Kore')"
    )
    instructions: Optional[str] = Field(
        default="", 
        description="Additional instructions for speech generation"
    )
    config: Optional[Dict[str, Any]] = Field(
        default=None, 
        description="Additional configuration parameters for the synthesizer"
    )


class ListAvailableVoicesRequest(BaseModel):
    """Request model for listing available voices with optional filters."""

    provider: Optional[str] = Field(
        default=None,
        description="Filter voices by provider name (e.g., 'openai', 'gemini').",
    )
    characteristic: Optional[str] = Field(
        default=None,
        description="Filter voices by characteristic (e.g., 'Bright', 'Firm', 'Friendly').",
    )


class GenerateConfigRequest(BaseModel):
    """Request model for generating a YAML configuration file using an LLM."""

    instructions: str = Field(
        ..., description="Instructions describing the desired speech configuration."
    )
    model: str = Field(
        default="gpt-5-mini",
        description="LLM model name to use for generation via LiteLLM.",
    )
    temperature: float = Field(
        default=1.0, description="Sampling temperature for the generation."
    )
    max_tokens: int = Field(
        default=10000,
        description="Maximum number of tokens to generate in the YAML output.",
    )