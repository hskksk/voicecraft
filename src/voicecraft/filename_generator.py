#!/usr/bin/env python3
"""
汎用的なファイル名生成機能とCLI

このモジュールは、テキストコンテンツから適切なファイル名を生成する機能を提供します。
OpenAI GPTモデルまたはGeminiモデルを使用して、コンテンツに基づいた意味のあるファイル名を生成できます。
"""

import argparse
import os
import sys
import hashlib
import datetime
import re
from typing import Optional, Union
import litellm


class FilenameGenerator:
    """ファイル名生成クラス"""
    
    def __init__(self, provider: str = "openai"):
        """
        ファイル名生成器を初期化
        
        Args:
            provider: 使用するプロバイダー ("openai" または "gemini")
            api_key: APIキー（Noneの場合は環境変数から取得）
        """
        self.provider = provider.lower()
        
        # プロバイダーに応じてモデルを選択
        if self.provider == "openai":
            self.model = "openai/gpt-5-nano"
            self.api_key = os.getenv('OPENAI_API_KEY')
        elif self.provider == "gemini":
            self.model = "gemini/gemini-2.5-flash-lite"
            self.api_key = os.getenv('GOOGLE_API_KEY')
        else:
            raise ValueError(f"Unsupported provider: {provider}. Use 'openai' or 'gemini'.")
    
    def generate_filename(self, content: str, extension: str = "txt", 
                         include_timestamp: bool = True, 
                         max_length: int = 50) -> str:
        """
        コンテンツから適切なファイル名を生成
        
        Args:
            content: ファイル名を生成するためのテキストコンテンツ
            extension: ファイル拡張子（ドットは含めない）
            include_timestamp: タイムスタンプを含めるかどうか
            max_length: 生成されるファイル名の最大長
            
        Returns:
            生成されたファイル名
        """
        try:
            generated_name = self._generate_with_litellm(content)
            
            # ファイル名をクリーンアップ
            safe_name = self._clean_filename(generated_name, max_length)
            
            # タイムスタンプを追加
            if include_timestamp:
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{safe_name}_{timestamp}.{extension}"
            else:
                filename = f"{safe_name}.{extension}"
            
            return filename
            
        except Exception as e:
            print(f"Warning: Failed to generate filename with {self.model}: {e}")
            print("Falling back to hash-based filename generation...")
            return self._generate_fallback_filename(content, extension, include_timestamp)
    
    def _generate_with_litellm(self, content: str) -> str:
        """LiteLLMを使用してファイル名を生成"""
        system_instruction = """テキストファイルのファイル名を作成してください。指示の中で、テキストファイルに含まれる文の内容を渡すので、それを元にファイル名を考えてください。ファイル名は英語で、短く、内容を表すものにしてください。拡張子は含めないでください。出力はファイル名を１つだけ返すようにしてください。"""
        
        response = litellm.completion(
            model=self.model,
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": f"以下の話の内容から適切なファイル名を作成してください:\n\n{content}"}
            ],
            reasoning_effort="low",
            max_tokens=1000
        )
        print(response)
        
        return response.choices[0].message.content.strip()
    
    def _clean_filename(self, filename: str, max_length: int) -> str:
        """ファイル名をクリーンアップ"""
        # ファイル名として使用できない文字を除去
        safe_name = re.sub(r'[<>:"/\\|?*]', '', filename)
        safe_name = safe_name.replace(' ', '_')
        
        # 長さを制限
        if len(safe_name) > max_length:
            safe_name = safe_name[:max_length]
        
        # 空の場合はデフォルト名を使用
        if not safe_name:
            safe_name = "generated_file"
        
        return safe_name
    
    def _generate_fallback_filename(self, content: str, extension: str, include_timestamp: bool) -> str:
        """フォールバック: ハッシュベースのファイル名生成"""
        content_hash = hashlib.md5(content.encode()).hexdigest()[:8]
        
        if include_timestamp:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            return f"file_{timestamp}_{content_hash}.{extension}"
        else:
            return f"file_{content_hash}.{extension}"


def main():
    """CLIメイン関数"""
    parser = argparse.ArgumentParser(
        description="Generate meaningful filenames from text content",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s -t "Hello, world!" -e mp3
  %(prog)s -f input.txt -e wav --provider gemini
  %(prog)s -t "Medical consultation notes" -e pdf --no-timestamp
  %(prog)s -f script.txt -e py --max-length 30 --provider openai
        """
    )
    
    # テキスト入力のオプション（相互排他）
    text_group = parser.add_mutually_exclusive_group(required=True)
    text_group.add_argument(
        '-t', '--text',
        help='Text content to generate filename from'
    )
    text_group.add_argument(
        '-f', '--file',
        help='Path to text file containing content to generate filename from'
    )
    
    # 出力設定
    parser.add_argument(
        '-e', '--extension',
        default='txt',
        help='File extension (default: txt)'
    )
    parser.add_argument(
        '--no-timestamp',
        action='store_true',
        help='Do not include timestamp in filename'
    )
    parser.add_argument(
        '--max-length',
        type=int,
        default=50,
        help='Maximum length of generated filename (default: 50)'
    )
    
    # プロバイダー設定
    parser.add_argument(
        '--provider',
        choices=['openai', 'gemini'],
        default='openai',
        help='AI provider to use for filename generation (default: openai). OpenAI uses gpt-4o-mini, Gemini uses gemini-2.5-flash-lite'
    )
    parser.add_argument(
        '--api-key',
        help='API key (can also be set via OPENAI_API_KEY or GOOGLE_API_KEY environment variable)'
    )
    
    args = parser.parse_args()
    
    # テキストを取得
    if args.text:
        content = args.text
    else:
        if not os.path.exists(args.file):
            print(f"Error: File '{args.file}' not found.")
            sys.exit(1)
        with open(args.file, 'r', encoding='utf-8') as f:
            content = f.read().strip()
    
    if not content:
        print("Error: No text content found.")
        sys.exit(1)
    
    try:
        # ファイル名生成器を初期化
        generator = FilenameGenerator(
            provider=args.provider,
            api_key=args.api_key
        )
        
        # ファイル名を生成
        filename = generator.generate_filename(
            content=content,
            extension=args.extension,
            include_timestamp=not args.no_timestamp,
            max_length=args.max_length
        )
        
        print(filename)
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
