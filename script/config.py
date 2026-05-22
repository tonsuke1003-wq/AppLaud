"""
config.py — AppLaud Windows設定ファイル
config.sh の代替。値を編集して使用してください。

パス設定はこのスクリプトの位置（AppLaud/script/）を基準に自動解決されます。
MyContextの作業フォルダにAppLaudをcloneした場合（[作業フォルダ]/AppLaud/）、
APIキーは [作業フォルダ]/02_設定/.env から自動読み込みされます。
"""

import os
from pathlib import Path

# ── .envローダー ────────────────────────────────────
def _load_env(path: Path):
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, _, v = line.partition("=")
            k, v = k.strip(), v.strip().strip('"').strip("'")
            if k and not os.environ.get(k):
                os.environ[k] = v

_SCRIPT_DIR = Path(__file__).parent           # AppLaud/script/
_APPLAUD_DIR = _SCRIPT_DIR.parent             # AppLaud/
_BASE_DIR = _APPLAUD_DIR.parent               # [作業フォルダ]/ （MyContextのルート）
_ENV_PATH = _BASE_DIR / "02_設定" / ".env"

# .envが見つからない場合、Mac従来セットアップ（~/Desktop/MyContext/）にフォールバック
if not _ENV_PATH.exists():
    _ENV_PATH = Path.home() / "Desktop" / "MyContext" / "02_設定" / ".env"
_load_env(_ENV_PATH)

# ── 設定（ここを変更してください）──────────────────────

# TODO: ボイスレコーダーのドライブ文字（例: "E:\\"）
# 空文字列にすると、接続された全リムーバブルドライブを対象にする
RECORDER_DRIVE = ""

# TODO: レコーダー内の音声ファイルサブディレクトリ（例: "RECORD"）
# ルート直下の場合は空文字列 ""
VOICE_FILES_SUBDIR = "RECORD"

# 音声ファイルの移動先（通常は変更不要）
AUDIO_DEST_DIR = str(_BASE_DIR / "06_AppLaud" / "audio")

# Markdown要約ファイルの出力先（通常は変更不要）
MARKDOWN_OUTPUT_DIR = str(_BASE_DIR / "06_AppLaud")

# プロンプトファイルのパス（通常は変更不要）
SUMMARY_PROMPT_FILE_PATH = str(_APPLAUD_DIR / "prompt" / "summary_prompt.txt")

# 処理済みファイルのログパス（通常は変更不要）
PROCESSED_LOG_FILE = str(_BASE_DIR / "06_AppLaud" / "processed_log.jsonl")

# 対象とする音声ファイルの拡張子
TARGET_EXTENSIONS = [".wav", ".mp3", ".m4a"]

# ── ここまで設定 ────────────────────────────────────

# APIキー（GOOGLE_API_KEY または GEMINI_API_KEY のどちらでも可）
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY") or ""
