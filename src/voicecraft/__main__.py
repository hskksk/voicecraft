import os
import sys
from pathlib import Path
import wave
import click
import yaml
from voicecraft.filename_generator import FilenameGenerator
from voicecraft.speech_synthesizer import synthesizer_factory
from voicecraft.config_generator import ConfigGenerator




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


def wave_file(filename, pcm, channels=1, rate=24000, sample_width=2):
    """WAVファイルを保存する"""
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(sample_width)
        wf.setframerate(rate)
        wf.writeframes(pcm)


def save_audio(audio_data: bytes, output_path: str):
    """音声データをWAVファイルに保存する"""
    try:
        wave_file(output_path, audio_data)
        print(f"Audio saved to: {output_path}")
    except Exception as e:
        print(f"Error saving audio: {e}")
        sys.exit(1)


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
def craft(config, override_text, override_output):
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
        base_filename = generator.generate_filename(content, extension="wav")
        output_path = f"outputs/{base_filename}"

    click.echo(f"Output path: {output_path}")
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

    save_audio(audio_data, output_path)


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
