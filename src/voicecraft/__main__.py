import os
import sys
from pathlib import Path
from typing import Literal

import click
import yaml
from voicecraft.audio_export import save_audio_bytes
from voicecraft.filename_generator import FilenameGenerator
from voicecraft.speech_synthesizer import synthesizer_factory
from voicecraft.config_generator import ConfigGenerator


OutputFormat = Literal["wav", "mp3", "m4a"]


def read_config_file(config_path: str) -> dict:
    """設定ファイルを読み込む"""
    if not os.path.exists(config_path):
        click.echo(f"Error: Config file '{config_path}' not found.", err=True)
        sys.exit(1)

    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        return config
    except yaml.YAMLError as e:
        click.echo(f"Error parsing YAML config file: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error reading config file: {e}", err=True)
        sys.exit(1)


def resolve_output_format(
    cli_format: str | None,
    cfg: dict,
    output_path: str,
) -> OutputFormat:
    """CLI > YAML > path extension > default wav."""
    if cli_format is not None:
        return cli_format.lower()  # type: ignore[return-value]
    yaml_fmt = cfg.get("output_format")
    if yaml_fmt is not None:
        s = str(yaml_fmt).lower().strip()
        if s in ("wav", "mp3", "m4a"):
            return s  # type: ignore[return-value]
        raise ValueError(
            f"Invalid output_format in config: {yaml_fmt!r} (expected 'wav', 'mp3', or 'm4a')"
        )
    if output_path:
        suff = Path(output_path).suffix.lower()
        if suff == ".mp3":
            return "mp3"
        if suff == ".m4a":
            return "m4a"
        if suff == ".wav":
            return "wav"
    return "wav"


def align_output_path(path: str, output_format: OutputFormat) -> str:
    """If path ends in .wav/.mp3/.m4a, align extension with output_format."""
    p = Path(path)
    suff = p.suffix.lower()
    known = {".wav", ".mp3", ".m4a"}
    if suff in known:
        return str(p.with_suffix(f".{output_format}"))
    return path


@click.group()
def cli():
    """VoiceCraft CLI with subcommands."""


@cli.command("craft")
@click.option('-c', '--config',
              help='Path to YAML configuration file')
@click.option('--override-text',
              help='Override text from config file')
@click.option('--override-output',
              help='Override output file from config file')
@click.option(
    '--output-format',
    type=click.Choice(['wav', 'mp3', 'm4a'], case_sensitive=False),
    default=None,
    help='Output file format (wav, mp3, or m4a). Overrides config file.',
)
def craft(config, override_text, override_output, output_format):
    """
    Generate speech from text using LiteLLM with various TTS models.

    Configuration is loaded from a YAML file. You can override specific settings
    using command line options.
    """
    cfg = read_config_file(config)

    text_content = override_text or cfg.get('text', '')
    output_path = override_output or cfg.get('output', '')
    instructions_content = cfg.get('instructions', '')

    model_config = cfg.get('model_config', {})
    model = model_config.get('name', 'openai/gpt-4o-audio-preview')
    model_settings = model_config.get('config', {})

    try:
        resolved_format = resolve_output_format(output_format, cfg, output_path)
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

    if not text_content:
        click.echo("Error: No text content specified in config file or via --override-text.", err=True)
        sys.exit(1)

    if os.path.exists(text_content):
        with open(text_content, 'r', encoding='utf-8') as f:
            content = f.read().strip()
    else:
        content = text_content

    if not content:
        click.echo("Error: No text content found.", err=True)
        sys.exit(1)

    if not output_path:
        generator = FilenameGenerator(provider="openai")
        base_filename = generator.generate_filename(
            content, extension=resolved_format
        )
        output_path = f"outputs/{base_filename}"
    else:
        output_path = align_output_path(output_path, resolved_format)

    click.echo(f"Output path: {output_path}")
    click.echo(f"Output format: {resolved_format}")
    click.echo(f"Generating speech for text: {content[:100]}{'...' if len(content) > 100 else ''}")
    click.echo(f"Model: {model}")
    click.echo(f"Config: {model_settings}")
    if instructions_content:
        click.echo(f"Instruction: {instructions_content[:100]}{'...' if len(instructions_content) > 100 else ''}")

    try:
        synthesizer = synthesizer_factory(model, model_settings)
        audio_data = synthesizer.synthesize(content, instructions_content)
    except Exception as e:
        click.echo(f"Error creating synthesizer or generating speech: {e}", err=True)
        sys.exit(1)

    response_format = model_settings.get('response_format', 'wav')
    sample_rate = int(model_settings.get('sample_rate', 24000))

    try:
        save_audio_bytes(
            audio_data,
            output_path,
            output_format=resolved_format,
            response_format=response_format,
            sample_rate=sample_rate,
        )
    except RuntimeError as e:
        click.echo(f"Error saving audio: {e}", err=True)
        sys.exit(1)

    click.echo(f"Audio saved to: {output_path}")


@cli.command("gen")
@click.option('--instructions', '-i', required=True, help='Instructions to guide YAML config generation')
@click.option('--output', '-o', type=click.Path(dir_okay=False, writable=True, path_type=str),
              default='speech_configs/generated_config.yaml',
              help='Output path for generated YAML config')
@click.option('--model', default='gpt-5-mini', show_default=True, help='LLM model for generation')
@click.option('--temperature', type=float, default=1.0, show_default=True, help='Sampling temperature')
@click.option('--max-tokens', type=int, default=10000, show_default=True, help='Max output tokens')
@click.option('--few-shot', type=click.Path(exists=True, dir_okay=False, readable=True, path_type=str),
              help='Optional path to a few-shot YAML example to guide generation')
def gen(instructions, output, model, temperature, max_tokens, few_shot):
    """Generate a YAML configuration using an LLM and save it to a file."""
    few_shot_path = Path(few_shot) if few_shot else None
    try:
        generator = ConfigGenerator(
            model_name=model,
            temperature=temperature,
            max_output_tokens=max_tokens,
            few_shot_path=few_shot_path,
        )
        out_path = Path(output)
        generator.generate_to_file(instructions, out_path)
        click.echo(f"Config generated: {out_path}")
    except Exception as e:
        click.echo(f"Error generating config: {e}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    cli()
