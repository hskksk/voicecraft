# VoiceCraft

AI-powered speech synthesis tool with multi-speaker support for OpenAI and Gemini models.

## Features

- **Multi-Provider Support**: OpenAI and Gemini TTS models
- **Multi-Speaker Support**: Create conversations with multiple distinct voices
- **Rich Voice Options**: 30+ Gemini voices with unique characteristics
- **YAML Configuration**: Flexible configuration management
- **Speaker Descriptions**: Detailed voice style instructions for each speaker
- **Automatic Filename Generation**: AI-powered intelligent naming

## Installation

```bash
# Install dependencies
uv sync
```

**MP3 / M4A output:** Encoding and decoding audio formats uses [ffmpeg-python](https://github.com/kkroening/ffmpeg-python), which requires [ffmpeg](https://ffmpeg.org/) installed and available on your `PATH`. WAV output also requires ffmpeg.

## Usage

### Basic Usage

```bash
# 音声生成
uv run voicecraft craft -c speech_configs/gemini_example.yaml
uv run voicecraft craft -c speech_configs/gemini_multi_speaker_example.yaml --override-output outputs/custom_name.wav
uv run voicecraft craft -c speech_configs/gemini_example.yaml --output-format mp3 --override-output outputs/custom_name.mp3

# テキストを直接上書き
uv run voicecraft craft -c speech_configs/gemini_example.yaml --override-text "Hello, world!"

# コンフィグ生成
uv run voicecraft gen -i "二人の対話でAIの最新動向、WAV、明瞭でフレンドリー" -o speech_configs/generated_config.yaml
uv run voicecraft gen -i "技術ニュース独白、1人、WAV" --few-shot speech_configs/gemini_multi_speaker_example.yaml
```

### `craft` Command Options

| Option | Description |
|---|---|
| `-c`, `--config` | Path to YAML configuration file |
| `--override-text` | Override the `text` field in the config file |
| `--override-output` | Override the output file path in the config file |
| `--output-format` | Output format: `wav`, `mp3`, or `m4a`. Overrides config file. |

### `gen` Command Options

| Option | Default | Description |
|---|---|---|
| `-i`, `--instructions` | *(required)* | Instructions to guide YAML config generation |
| `-o`, `--output` | `speech_configs/generated_config.yaml` | Output path for generated YAML config |
| `--model` | `gpt-5-mini` | LLM model used for generation |
| `--temperature` | `1.0` | Sampling temperature |
| `--max-tokens` | `10000` | Max output tokens |
| `--few-shot` | | Path to a YAML example to guide generation |

### Configuration Files

VoiceCraft uses YAML configuration files for flexible speech generation:

```yaml
# Text content — can also be a path to a text file
text: |
  Hello, this is a sample text for speech generation.

# Instructions
instructions: |
  Please speak naturally and clearly.

# Optional: file format on disk (wav, mp3, or m4a). CLI --output-format overrides this.
# output_format: mp3

# Model configuration
model_config:
  name: "gemini-2.5-flash-preview-tts"
  config:
    multi_speaker: false
    voice: "Kore"  # Firm
    response_format: "wav"
    sample_rate: 24000  # Optional, default: 24000
```

#### Output Format Resolution Order

When multiple sources specify the output format, the following priority applies:

1. CLI `--output-format`
2. `output_format` field in YAML config
3. Extension of the output file path (`.wav`, `.mp3`, `.m4a`)
4. Default: `wav`

#### Text from File

The `text` field accepts either inline text or a file path. If the value is an existing file path, VoiceCraft reads the file contents:

```yaml
text: scripts/my_script.txt
```

### Multi-Speaker Configuration

```yaml
text: |
  Alice: Hello Bob, how are you?
  Bob: I'm doing great, thanks for asking!

model_config:
  name: "gemini-2.5-flash-preview-tts"
  config:
    multi_speaker: true
    speakers:
      - name: "Alice"
        voice_name: "Achird"  # フレンドリー
        description: "Friendly and enthusiastic speaker"
      - name: "Bob"
        voice_name: "Charon"  # 情報が豊富
        description: "Knowledgeable and calm speaker"
```

### Available Gemini Voices

**Bright**: Zephyr, Autonoe  
**Upbeat**: Puck, Laomedeia  
**Informative**: Charon, Rasalgethi, Sadaltager  
**Firm**: Kore, Orus, Alnilam  
**Excitable**: Fenrir  
**Youthful**: Leda  
**Breezy**: Aoede  
**Relaxed**: Callirrhoe, Umbriel  
**Breathy**: Enceladus  
**Clear**: Iapetus, Erinome  
**Smooth**: Algieba, Despina  
**Gravelly**: Algenib  
**Soft**: Achernar  
**Even**: Schedar  
**Mature**: Gacrux  
**Forward**: Pulcherrima  
**Friendly**: Achird  
**Casual**: Zubenelgenubi  
**Gentle**: Vindemiatrix  
**Lively**: Sadachbia  
**Warm**: Sulafat

## Examples

```bash
# Basic single-speaker generation
uv run voicecraft craft -c speech_configs/gemini_example.yaml

# Multi-speaker conversation
uv run voicecraft craft -c speech_configs/gemini_multi_speaker_example.yaml

# Pharmacy consultation example
uv run voicecraft craft -c speech_configs/pharmacy_consultation.yaml

# Voice showcase with different characteristics
uv run voicecraft craft -c speech_configs/gemini_voice_showcase.yaml

# Output as MP3
uv run voicecraft craft -c speech_configs/gemini_example.yaml --output-format mp3

# Output as M4A
uv run voicecraft craft -c speech_configs/gemini_example.yaml --output-format m4a
```

## Environment Setup

Set up your API keys as environment variables:

```bash
# For OpenAI models
export OPENAI_API_KEY="your-openai-api-key"

# For Gemini models
export GEMINI_API_KEY="your-google-api-key"
```

## Project Structure

```
voicecraft/
├── src/
│   └── voicecraft/
│       ├── __main__.py                   # CLI entrypoint
│       ├── audio_export.py               # Audio encoding / export
│       ├── config_generator.py           # LLM-based YAML config generator
│       ├── filename_generator.py         # Automatic filename generation
│       └── speech_synthesizer/           # Speech synthesis modules
│           ├── base.py                   # Abstract base class
│           ├── openai_synthesizer.py     # OpenAI implementation
│           ├── gemini_synthesizer.py     # Gemini implementation
│           ├── gemini_voices.py          # Gemini voice definitions
│           ├── factory.py                # Synthesizer factory
│           └── __init__.py
├── speech_configs/                       # YAML configuration examples
│   ├── gemini_example.yaml
│   ├── gemini_multi_speaker_example.yaml
│   ├── gemini_voice_showcase.yaml
│   ├── pharmacy_consultation.yaml
│   └── gemini_detailed_speakers.yaml
├── outputs/                              # Generated audio files
└── pyproject.toml                        # Project configuration
```

## License

MIT License
