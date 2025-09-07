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

## Usage

### Basic Usage

```bash
# 音声生成
uv run voicecraft craft -c speech_configs/gemini_example.yaml
uv run voicecraft craft -c speech_configs/gemini_multi_speaker_example.yaml --override-output outputs/custom_name.wav

# コンフィグ生成
uv run voicecraft gen -i "二人の対話でAIの最新動向、WAV、明瞭でフレンドリー" -o speech_configs/generated_config.yaml
uv run voicecraft gen -i "技術ニュース独白、1人、WAV" --few-shot speech_configs/gemini_multi_speaker_example.yaml
```

### Configuration Files

VoiceCraft uses YAML configuration files for flexible speech generation:

```yaml
# Text content
text: |
  Hello, this is a sample text for speech generation.

# Instructions
instructions: |
  Please speak naturally and clearly.

# Model configuration
model_config:
  name: "gemini-2.5-flash-preview-tts"
  config:
    multi_speaker: false
    voice: "Kore"  # Firm
    response_format: "wav"
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
python main.py --config speech_configs/gemini_example.yaml

# Multi-speaker conversation
python main.py --config speech_configs/gemini_multi_speaker_example.yaml

# Pharmacy consultation example
python main.py --config speech_configs/pharmacy_consultation.yaml

# Voice showcase with different characteristics
python main.py --config speech_configs/gemini_voice_showcase.yaml
```

## Environment Setup

Set up your API keys as environment variables:

```bash
# For OpenAI models
export OPENAI_API_KEY="your-openai-api-key"

# For Gemini models
export GOOGLE_API_KEY="your-google-api-key"
```

## Project Structure

```
voicecraft/
├── main.py                           # Main CLI application
├── src/
│   └── speech_synthesizer/           # Speech synthesis modules
│       ├── base.py                   # Abstract base class
│       ├── openai_synthesizer.py     # OpenAI implementation
│       ├── gemini_synthesizer.py     # Gemini implementation
│       ├── gemini_voices.py          # Gemini voice definitions
│       ├── factory.py                # Synthesizer factory
│       └── __init__.py
├── speech_configs/                   # YAML configuration examples
│   ├── gemini_example.yaml
│   ├── gemini_multi_speaker_example.yaml
│   ├── gemini_voice_showcase.yaml
│   ├── pharmacy_consultation.yaml
│   └── gemini_detailed_speakers.yaml
├── outputs/                          # Generated audio files
└── pyproject.toml                    # Project configuration
```

## License

MIT License
