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
STATE_FILE  = BASE_DIR / "07_タスク" / ".extract_tasks_state.json"
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

FALLBACK_GEMINI_MODEL = "gemini-flash-latest"   # .env に GEMINI_MODEL が無い場合のみ使う

def get_gemini_model() -> str:
    env = load_env(ENV_PATH)
    return env.get("GEMINI_MODEL", "") or os.environ.get("GEMINI_MODEL", "") or FALLBACK_GEMINI_MODEL

def extract_gemini_text(data: dict) -> str:
    """Geminiのレスポンスから本文テキストを取り出す。

    Gemini 3系は thinking がデフォルトで有効。parts[0] が思考パート（textキー無し）だったり、
    出力上限に当たって text が1つも返らないことがあるため、
    parts[0]["text"] の直参照は KeyError で落ちる。必ず全partsを走査する。
    """
    for cand in data.get("candidates", []):
        parts = cand.get("content", {}).get("parts", []) or []
        texts = [pt["text"] for pt in parts
                 if isinstance(pt, dict) and pt.get("text") and not pt.get("thought")]
        if texts:
            return "\n".join(texts).strip()
        if cand.get("finishReason") == "MAX_TOKENS":
            print("  ⚠️ 出力上限に到達（maxOutputTokensを増やしてください）", file=sys.stderr)
    return ""

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
        "generationConfig": {"maxOutputTokens": 4096, "temperature": 0.2},
    }, ensure_ascii=False).encode("utf-8")

    model = get_gemini_model()
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as res:
            result = extract_gemini_text(json.load(res))
            if not result or result == "タスクなし":
                return []
            return [l.strip() for l in result.splitlines() if l.strip()]
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

# ── 重複防止 ────────────────────────────────────────────────
# 「AppLaudからタスク抽出」を2回言うと同じタスクが二重に増えるのを防ぐ。
# 2段構えにしている:
#   ① ファイル単位 … 一度処理した音声メモは (ファイル名, 更新時刻) を記録してスキップ
#   ② タスク単位  … MASTER_TASKS.md に同じ文面が既にあれば追加しない
# ①だけだとファイルが編集された時に全タスクが再追加されるため、②が最後の砦になる。

def load_state() -> dict:
    try:
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    except Exception:
        return {"processed": {}}

def save_state(state: dict) -> None:
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")

def normalize_task(text: str) -> str:
    """重複判定用の正規化。空白・記号・「（AppLaud: 日付）」注記を落とす。"""
    text = re.sub(r"（AppLaud:[^）]*）", "", text)
    text = re.sub(r"[\s\u3000・\-\*。、,.．]+", "", text)
    return text

def existing_task_keys() -> set:
    """MASTER_TASKS.md に既に載っているタスク文の集合を返す。"""
    if not TASKS_FILE.exists():
        return set()
    keys = set()
    for line in TASKS_FILE.read_text(encoding="utf-8", errors="ignore").splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) >= 2 and cells[1] and cells[1] != "タスク":
            key = normalize_task(cells[1])
            if key:
                keys.add(key)
    return keys

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
    force = "--force" in sys.argv
    print("=== AppLaud → MASTER_TASKS 連携 ===")
    if force:
        print("(--force: 処理済み記録を無視して再抽出します)")

    env = load_env(ENV_PATH)
    api_key = env.get("GEMINI_API_KEY", "") or os.environ.get("GEMINI_API_KEY", "")
    files = get_recent_applaud_files(days=1)
    if not files:
        print(f"直近24時間のAppLaudファイルが見つかりません: {APPLAUD_DIR}")
        return

    state = load_state()
    processed = state.get("processed", {})
    known = existing_task_keys()   # MASTER_TASKS.md に既にあるタスク

    print(f"対象ファイル: {len(files)}件")
    total_added = total_dup = skipped_files = 0

    for f in files:
        signature = str(f.stat().st_mtime_ns)
        if not force and processed.get(f.name) == signature:
            skipped_files += 1
            continue

        print(f"\n処理中: {f.name}")
        text = f.read_text(encoding="utf-8", errors="ignore")
        tasks = extract_tasks_with_gemini(text, api_key) if api_key else extract_tasks_simple(text)
        method = "Gemini" if api_key else "キーワード抽出"
        processed[f.name] = signature

        if not tasks:
            print(f"  タスクなし（{method}）")
            continue

        # タスク単位の重複除去（同じ実行内での重複もここで落ちる）
        fresh = []
        for t in tasks:
            key = normalize_task(t)
            if not key or key in known:
                total_dup += 1
                continue
            known.add(key)
            fresh.append(t)

        if not fresh:
            print(f"  抽出 {len(tasks)}件 — すべて登録済みのためスキップ（{method}）")
            continue

        print(f"  新規タスク ({method}): {len(fresh)}件" +
              (f" / 重複スキップ {len(tasks) - len(fresh)}件" if len(tasks) != len(fresh) else ""))
        for t in fresh:
            print(f"    - {t}")
        total_added += append_tasks_to_master(fresh)

    state["processed"] = processed
    save_state(state)

    if skipped_files:
        print(f"\n処理済みのためスキップしたファイル: {skipped_files}件（再抽出したい場合は --force）")
    if total_added > 0:
        print(f"✅ MASTER_TASKS.mdに {total_added}件 追加しました: {TASKS_FILE}")
    else:
        print("追加されたタスクはありませんでした")
    if total_dup:
        print(f"（重複として除外したタスク: {total_dup}件）")

if __name__ == "__main__":
    main()
