from __future__ import annotations

from pathlib import Path
from typing import Optional

from litellm import completion


class ConfigGenerator:
    """Generate speech config YAMLs using an LLM with a few-shot example.

    This class loads the `speech_configs/gemini_multi_speaker_example.yaml` as a
    few-shot exemplar and prompts `gpt-5-mini` (via LiteLLM) to produce a new YAML
    configuration based on user-provided instructions.
    """

    def __init__(
        self,
        model_name: str = "gpt-5-mini",
        temperature: float = 1,
        max_output_tokens: int = 10000,
        few_shot_path: Optional[Path] = None,
    ) -> None:
        self.model_name = model_name
        self.temperature = temperature
        self.max_output_tokens = max_output_tokens
        self.few_shot_path = (
            few_shot_path if few_shot_path is not None else self._default_few_shot_path()
        )

        if not self.few_shot_path.exists():
            raise FileNotFoundError(f"Few-shot example not found: {self.few_shot_path}")

        self._few_shot_yaml = self.few_shot_path.read_text(encoding="utf-8")

    def _default_few_shot_path(self) -> Path:
        # Project root is two parents up from this file: src/voicecraft/.. -> src -> project root
        project_root = Path(__file__).resolve().parents[2]
        return project_root / "speech_configs" / "gemini_multi_speaker_example.yaml"

    def generate_config(self, user_instructions: str) -> str:
        """Generate a YAML configuration string from instructions.

        Returns a YAML string. The model is prompted to return ONLY YAML.
        """
        system_prompt = (
            "You are a helpful assistant that generates YAML configuration files for "
            "a speech synthesis tool. Output must be valid YAML only with no prose."
        )

        # Few-shot: provide the example YAML as an assistant message to show ideal format
        messages = [
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": (
                    "Here is an example YAML config for multi-speaker Gemini text to speech. "
                    "Follow this structure."
                ),
            },
            {"role": "assistant", "content": self._few_shot_yaml},
            {
                "role": "user",
                "content": (
                    "Using the same structure, generate a new YAML config based on "
                    "these instructions. Return YAML only, no explanations.\n\n"
                    f"Instructions:\n{user_instructions}"
                ),
            },
        ]

        response = completion(
            model=self.model_name,
            messages=messages,
            temperature=self.temperature,
            max_tokens=self.max_output_tokens,
        )

        # LiteLLM returns a dict similar to OpenAI
        print(response)
        content = response["choices"][0]["message"]["content"]
        return content.strip()

    def generate_to_file(self, user_instructions: str, output_path: Path) -> Path:
        """Generate YAML from instructions and write to a file.

        Returns the output path.
        """
        yaml_text = self.generate_config(user_instructions=user_instructions)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(yaml_text, encoding="utf-8")
        return output_path


