#!/usr/bin/env python3
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
"""
extract_tasks.py
AppLaudの出力（./06_AppLaud/）からタスクを抽出し、
./07_タスク/MASTER_TASKS.md に追記する。

使い方: python3 ./AppLaud/script/extract_tasks.py
"""

import os
import re
import sys
import json
from datetime import datetime
from pathlib import Path

# スクリプト位置から自動でプロジェクトルートを決定
# AppLaud/script/ → AppLaud/ → [作業フォルダ]/
BASE_DIR    = Path(__file__).parent.parent.parent
APPLAUD_DIR = BASE_DIR / "06_AppLaud"
TASKS_FILE  = BASE_DIR / "07_タスク" / "MASTER_TASKS.md"
ENV_PATH    = BASE_DIR / "02_設定" / ".env"

def load_env(path: Path) -> dict:
    env = {}
    try:
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip().strip('"').strip("'")
    except Exception:
        pass
    return env

def get_recent_applaud_files(days: int = 1) -> list[Path]:
    if not APPLAUD_DIR.exists():
        return []
    files = sorted(APPLAUD_DIR.glob("*.md"), key=lambda f: f.stat().st_mtime, reverse=True)
    cutoff = datetime.now().timestamp() - (days * 86400)
    return [f for f in files if f.stat().st_mtime >= cutoff]

def extract_tasks_with_gemini(text: str, api_key: str) -> list[str]:
    import urllib.request

    prompt = f"""以下は音声メモの文字起こしです。
この中から「タスク・やること・TODO」に相当するものをすべて抽出してください。
【ルール】
- 1行1タスクで出力
- 箇条書き記号（- や ・）は不要。タスク本文だけ出力
- タスクが見つからない場合は「タスクなし」と出力

【文字起こし】
{text[:3000]}
"""

    payload = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"maxOutputTokens": 1024, "temperature": 0.2},
    }, ensure_ascii=False).encode("utf-8")

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent?key={api_key}"
    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as res:
            data = json.load(res)
            result = data["candidates"][0]["content"]["parts"][0]["text"].strip()
            return [] if result == "タスクなし" else [l.strip() for l in result.splitlines() if l.strip()]
    except Exception as e:
        print(f"  Gemini APIエラー: {e}", file=sys.stderr)
        return []

def extract_tasks_simple(text: str) -> list[str]:
    task_keywords = ["する", "やる", "確認", "連絡", "送る", "作る", "調べる", "提出", "返信", "予約"]
    tasks = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        if re.match(r'^[・\-\*]|^TODO|^タスク', line):
            tasks.append(re.sub(r'^[・\-\*\s]+', '', line))
        elif len(line) < 50 and any(kw in line for kw in task_keywords):
            tasks.append(line)
    return tasks

def append_tasks_to_master(tasks: list[str]) -> int:
    if not tasks:
        return 0
    today = datetime.now().strftime("%Y-%m-%d")
    TASKS_FILE.parent.mkdir(parents=True, exist_ok=True)
    content = TASKS_FILE.read_text(encoding="utf-8") if TASKS_FILE.exists() else \
        "# MASTER_TASKS.md — タスク管理\n\n## 🟡 優先度B（今月中）\n\n| # | タスク | 期限 | 状態 |\n|---|---|---|---|\n"
    new_rows = [f"|   | {t}（AppLaud: {today}） |   | 📥 未着手 |" for t in tasks]
    marker = "## 🟡 優先度B（今月中）"
    if marker in content:
        header_pos = content.find("| # | タスク | 期限 | 状態 |", content.find(marker))
        if header_pos != -1:
            sep_end = content.find("\n", content.find("\n", header_pos) + 1)
            content = content[:sep_end + 1] + "\n".join(new_rows) + "\n" + content[sep_end + 1:]
        else:
            content += "\n" + "\n".join(new_rows) + "\n"
    else:
        content += f"\n{marker}\n\n| # | タスク | 期限 | 状態 |\n|---|---|---|---|\n" + "\n".join(new_rows) + "\n"
    TASKS_FILE.write_text(content, encoding="utf-8")
    return len(tasks)

def main():
    print("=== AppLaud → MASTER_TASKS 連携 ===")
    env = load_env(ENV_PATH)
    api_key = env.get("GEMINI_API_KEY", "") or os.environ.get("GEMINI_API_KEY", "")
    files = get_recent_applaud_files(days=1)
    if not files:
        print(f"直近24時間のAppLaudファイルが見つかりません: {APPLAUD_DIR}")
        return
    print(f"対象ファイル: {len(files)}件")
    total_added = 0
    for f in files:
        print(f"\n処理中: {f.name}")
        text = f.read_text(encoding="utf-8", errors="ignore")
        tasks = extract_tasks_with_gemini(text, api_key) if api_key else extract_tasks_simple(text)
        method = "Gemini" if api_key else "キーワード抽出"
        if not tasks:
            print(f"  タスクなし（{method}）")
            continue
        print(f"  抽出タスク ({method}): {len(tasks)}件")
        for t in tasks:
            print(f"    - {t}")
        total_added += append_tasks_to_master(tasks)
    if total_added > 0:
        print(f"\n✅ MASTER_TASKS.mdに {total_added}件 追加しました: {TASKS_FILE}")
    else:
        print("\n追加されたタスクはありませんでした")

if __name__ == "__main__":
    main()
