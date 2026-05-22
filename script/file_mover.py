#!/usr/bin/env python3
"""
file_mover.py — AppLaud Windows版ファイル移動スクリプト
file_mover.sh の代替。

処理内容:
1. 指定されたドライブパスから音声ファイルを検索する
2. 音声ファイルをローカルフォルダに移動する
3. transcribe_summarize.py を呼び出して文字起こし・要約を実行する

使用法:
  python file_mover.py <ドライブパス>
  例: python file_mover.py E:\\
  例: python file_mover.py "E:\\"
"""

import sys
import shutil
import subprocess
from pathlib import Path

# config.py から設定を読み込む
sys.path.insert(0, str(Path(__file__).parent))
from config import (
    VOICE_FILES_SUBDIR,
    AUDIO_DEST_DIR,
    MARKDOWN_OUTPUT_DIR,
    SUMMARY_PROMPT_FILE_PATH,
    PROCESSED_LOG_FILE,
    TARGET_EXTENSIONS,
)


def find_audio_files(search_path: Path) -> list[Path]:
    audio_files = []
    for ext in TARGET_EXTENSIONS:
        audio_files.extend(search_path.rglob(f"*{ext}"))
        audio_files.extend(search_path.rglob(f"*{ext.upper()}"))
    # ._xxx のような隠しファイルを除外（Mac互換ファイルなど）
    return [f for f in audio_files if not f.name.startswith("._")]


def main():
    if len(sys.argv) < 2:
        print("使用法: python file_mover.py <ドライブパス>")
        print("例:     python file_mover.py E:\\\\")
        sys.exit(1)

    drive_path = Path(sys.argv[1])

    # 検索パスを決定
    search_path = drive_path / VOICE_FILES_SUBDIR if VOICE_FILES_SUBDIR else drive_path
    print(f"検索パス: {search_path}")

    # マウントポイントが存在するまで最大30秒待機
    import time
    for attempt in range(30):
        if search_path.exists():
            break
        print(f"待機中... ({attempt + 1}/30)")
        time.sleep(1)
    else:
        print(f"エラー: パスが30秒以内に利用可能になりませんでした: {search_path}")
        sys.exit(1)

    # 音声ファイルを検索
    audio_files = find_audio_files(search_path)
    if not audio_files:
        print(f"音声ファイルが見つかりませんでした: {search_path}")
        return

    print(f"検出された音声ファイル: {len(audio_files)}件")
    for f in audio_files:
        print(f"  - {f}")

    # ディレクトリを作成
    dest_dir = Path(AUDIO_DEST_DIR)
    markdown_dir = Path(MARKDOWN_OUTPUT_DIR)
    dest_dir.mkdir(parents=True, exist_ok=True)
    markdown_dir.mkdir(parents=True, exist_ok=True)
    Path(PROCESSED_LOG_FILE).parent.mkdir(parents=True, exist_ok=True)
    Path(PROCESSED_LOG_FILE).touch(exist_ok=True)

    print(f"\n音声ファイル保存先: {dest_dir}")
    print(f"Markdown出力先: {markdown_dir}")

    # ファイルを移動
    print("\n--- ファイル移動 ---")
    for audio_file in audio_files:
        dest_path = dest_dir / audio_file.name
        print(f"移動: {audio_file.name}")
        try:
            shutil.move(str(audio_file), str(dest_path))
            print(f"  → {dest_path}")
        except Exception as e:
            print(f"  エラー: {e}")

    # transcribe_summarize.py を呼び出す
    script_dir = Path(__file__).parent
    transcribe_script = script_dir / "transcribe_summarize.py"

    print(f"\n--- 文字起こし・要約処理 ---")
    print(f"スクリプト: {transcribe_script}")

    result = subprocess.run([
        sys.executable, str(transcribe_script),
        "--audio_processing_dir", str(dest_dir),
        "--markdown_output_dir", str(markdown_dir),
        "--summary_prompt_file_path", SUMMARY_PROMPT_FILE_PATH,
        "--processed_log_file_path", PROCESSED_LOG_FILE,
    ])

    if result.returncode == 0:
        print("\n✅ 全ての処理が完了しました。")
    else:
        print(f"\n❌ エラー: 処理が失敗しました (終了コード: {result.returncode})")
        sys.exit(result.returncode)


if __name__ == "__main__":
    main()
