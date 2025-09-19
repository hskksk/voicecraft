from typing import Optional
from pydantic import BaseModel, Field


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