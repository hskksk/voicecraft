# VoiceCraft MCP Implementation Plan

## 概要
VoiceCraftのCLI機能を分析し、MCP (Model Context Protocol) のtool、resource、promptとして最適に実装する計画を策定しました。

## VoiceCraft CLI機能分析

### 主要コマンド
1. **`craft`** - 音声合成メイン機能
   - YAML設定ファイルから音声生成
   - テキスト・出力パスの上書きオプション
   - マルチスピーカー対応

2. **`gen`** - 設定ファイル生成
   - LLMを使用したYAML設定の自動生成
   - Few-shot学習サポート
   - カスタマイズ可能なパラメータ

3. **`serve`** - APIサーバー起動
   - FastAPIベースのWeb API
   - 開発・本番モード対応

### サポート機能
- **FilenameGenerator**: AI駆動のファイル名生成
- **ConfigGenerator**: LLMベースの設定生成
- **SpeechSynthesizer**: マルチプロバイダー音声合成
- **Gemini Voices**: 30+の音声オプション

## MCP実装計画

### 1. Tools (ツール)

#### 1.1 `synthesize`
**目的**: メインの音声合成機能（現在はスタブ実装）
```python
def synthesize(
    text: str,
    model: Optional[str],
    voice: Optional[str],
    config: Optional[Dict[str, Any]] = None,
) -> SynthesisResponse:
    """
    Generate speech from text using VoiceCraft
    
    Args:
        text: Text content to synthesize
        model: Model name (provider/model or alias)
        voice: Voice name for single speaker
        config: Additional synthesizer configuration
    
    Returns:
        SynthesisResponse pydantic model
    """
```

#### 1.2 `generate_config`
**目的**: YAML設定ファイルの自動生成
```python
def generate_config(
    instructions: str,
    output_path: str = "speech_configs/generated_config.yaml",
    model: str = "gpt-4o-mini",
    temperature: float = 1.0,
    max_tokens: int = 10000,
    few_shot_example: Optional[str] = None
) -> Dict[str, Any]:
    """
    Generate YAML configuration file using LLM
    
    Args:
        instructions: Instructions for config generation
        output_path: Output file path
        model: LLM model for generation
        temperature: Sampling temperature
        max_tokens: Maximum output tokens
        few_shot_example: Path to example config file
    
    Returns:
        Dict containing:
        - success: bool
        - config_path: str
        - config_content: str
        - message: str
    """
```

#### 1.3 `generate_filename`
**目的**: AI駆動のファイル名生成
```python
def generate_filename(
    content: str,
    extension: str = "wav",
    provider: str = "openai",
    include_timestamp: bool = True,
    max_length: int = 50
) -> Dict[str, Any]:
    """
    Generate meaningful filename from content
    
    Args:
        content: Text content to generate filename from
        extension: File extension
        provider: AI provider (openai, gemini)
        include_timestamp: Include timestamp in filename
        max_length: Maximum filename length
    
    Returns:
        Dict containing:
        - success: bool
        - filename: str
        - full_path: str
        - message: str
    """
```

#### 1.4 `list_available_models`
**目的**: 利用可能なモデル一覧取得
```python
def list_available_models() -> Dict[str, Any]:
    """
    List all available speech synthesis models
    
    Returns:
        Dict containing:
        - models: List[Dict] with model info (provider, voices, formats など)
        - providers: List[str] of supported providers
    """
```

#### 1.5 `list_available_voices`
**目的**: 利用可能な音声一覧取得（プロバイダと特徴でフィルタ）
```python
def list_available_voices(
    provider: Optional[str] = None,
    characteristic: Optional[str] = None
) -> Dict[str, Any]:
    """
    List available voices for speech synthesis
    
    Args:
        provider: Filter by provider name (e.g., "openai", "gemini")
        characteristic: Filter by voice characteristic (e.g., "Bright", "Firm")
    
    Returns:
        Dict containing:
        - voices: List[Dict] with voice info
        - characteristics: List[str] of available characteristics
        - providers: List[str] of providers present in result
    """
```

#### 1.6 `list_available_providers`
**目的**: 利用可能なTTSプロバイダ一覧取得
```python
def list_available_providers() -> Dict[str, Any]:
    """
    List all available TTS providers supported by VoiceCraft
    
    Returns:
        Dict containing:
        - providers: List[Dict] with provider information
        - total_providers: Number of available providers
    """
```

## 実装優先順位

### Phase 1: 基本機能
1. `list_available_models` tool
2. `list_available_voices` tool
3. `list_available_providers` tool

### Phase 2: 高度な機能
1. `generate_config` tool
2. `generate_filename` tool

### Phase 3: 複雑な機能
1. `synthesize` tool（スタブから本実装へ拡張予定）

## 技術的考慮事項

### エラーハンドリング
- 適切なHTTPステータスコード
- 詳細なエラーメッセージ
- ログ記録

### パフォーマンス
- 非同期処理の活用
- キャッシュ戦略
- リソース管理

### セキュリティ
- APIキーの適切な管理
- 入力検証
- レート制限

### 拡張性
- プラグインアーキテクチャ
- 設定の外部化
- モジュラー設計

## 統合ポイント

### 既存機能との連携
- `synthesizer_factory`との統合
- `ConfigGenerator`との統合
- `FilenameGenerator`との統合

### 設定管理
- 環境変数の活用
- 設定ファイルの読み込み
- デフォルト値の管理

この計画に基づいて、段階的にMCP実装を進めることで、VoiceCraftの全機能をMCP経由で利用可能にします。
