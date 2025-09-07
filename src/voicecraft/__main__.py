import os
import sys
from pathlib import Path
import wave
import click
import yaml
from voicecraft.filename_generator import FilenameGenerator
from voicecraft.speech_synthesizer import synthesizer_factory




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


@click.command()
@click.option('-c', '--config', 
              help='Path to YAML configuration file')
@click.option('--override-text', 
              help='Override text from config file')
@click.option('--override-output', 
              help='Override output file from config file')
def cli(config, override_text, override_output):
    """
    Generate speech from text using LiteLLM with various TTS models.
    
    Configuration is loaded from a YAML file. You can override specific settings
    using command line options.
    
    Examples:
      main.py                                    # Use default config file
      main.py -c my_config.yaml                  # Use custom config file
      main.py --override-text "Hello!"           # Override text from config
      main.py --override-output "output.wav"     # Override output file
    
    Available models: gpt-4o-audio-preview, gemini-2.5-flash-preview-tts, etc.
    Available voices: alloy, echo, fable, onyx, nova, shimmer (for OpenAI), Kore, Puck (for Gemini)
    """
    # 設定ファイルを読み込み
    config = read_config_file(config)
    
    # 設定から値を取得（オーバーライド可能）
    text_content = override_text or config.get('text', '')
    output_path = override_output or config.get('output', '')
    instructions_content = config.get('instructions', '')
    
    # モデル設定を取得
    model_config = config.get('model_config', {})
    model = model_config.get('name', 'openai/gpt-4o-audio-preview')
    model_settings = model_config.get('config', {})
    
    # テキストコンテンツを取得
    if not text_content:
        click.echo("Error: No text content specified in config file or via --override-text.", err=True)
        sys.exit(1)
    
    # テキストがファイルパスの場合、ファイルから読み込み
    if os.path.exists(text_content):
        with open(text_content, 'r', encoding='utf-8') as f:
            content = f.read().strip()
    else:
        content = text_content
    
    if not content:
        click.echo("Error: No text content found.", err=True)
        sys.exit(1)
    
    # 出力ファイル名を決定
    if not output_path:
        # 自動生成されたファイル名を使用
        generator = FilenameGenerator(provider="openai")
        base_filename = generator.generate_filename(content, extension="wav")
        output_path = f"outputs/{base_filename}"
    
    click.echo(f"Output path: {output_path}")
    
    # 指示は設定ファイルから直接取得
    
    click.echo(f"Generating speech for text: {content[:100]}{'...' if len(content) > 100 else ''}")
    click.echo(f"Model: {model}")
    click.echo(f"Config: {model_settings}")
    if instructions_content:
        click.echo(f"Instruction: {instructions_content[:100]}{'...' if len(instructions_content) > 100 else ''}")
    
    # 音声合成器を作成
    try:
        synthesizer = synthesizer_factory(model, model_settings)
        audio_data = synthesizer.synthesize(content, instructions_content)
    except Exception as e:
        click.echo(f"Error creating synthesizer or generating speech: {e}", err=True)
        sys.exit(1)
    
    # 音声を保存
    save_audio(audio_data, output_path)


if __name__ == "__main__":
    cli()
