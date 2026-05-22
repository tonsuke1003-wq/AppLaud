私専用のコンテキストシステム「MyContext」を構築してください。
以下のステップを順番に、すべて完了するまで止まらず実行してください。

---

## Step 0: OSを確認する（自動分岐の準備）

以下を実行してOSを確認してください：

python3 -c "import platform; print(platform.system())"

出力を確認してください：
- `Darwin`  → **Mac** として以降を実行
- `Windows` → **Windows** として以降を実行

以降、`▶ Mac のみ` と書かれたセクションはMacのみ実行、`▶ Windows のみ` はWindowsのみ実行してください。
それ以外のセクションは **両OS共通** です。

---

## Step 1: フォルダ構造を作成する【共通】

**現在の作業フォルダ（このClaude Codeセッションのカレントディレクトリ）**に以下のフォルダをすべて作成してください。

[作業フォルダ]/
├── 00_ゴミ箱/
├── 01_事業・クライアント/
├── 02_設定/
├── 03_私について/
│   ├── 信念/
│   └── [AI名]/
├── 04_ナレッジ/
│   ├── 情報源/
│   ├── 切り抜き/
│   └── Vault/
├── 05_日記/
│   ├── チャットログ/
│   └── 週次まとめ/
├── 06_AppLaud/
├── 07_タスク/
└── .claude/

---

## Step 2: .env ファイルを作成する【共通】

`./02_設定/.env` を作成してください。
内容は以下のみ（値は私があとでエディタで直接入力します）：

```
GEMINI_API_KEY=
```

---

## Step 3: my_profile.md を作成する（Q&A対話）【共通】

まず、作業フォルダ内に AI秘書構築のフォルダが存在するか確認してください：

```python
from pathlib import Path
candidates = [d for d in Path('.').iterdir() if d.is_dir() and d.name.startswith('momon-secretary-starter')]
print(candidates[0] if candidates else 'NOT_FOUND')
```

**フォルダが見つかった場合:**
そのフォルダ内のすべてのMarkdownファイル（CLAUDE.md、profile.md、README.mdなど）を読み込み、以下の7項目に関連する情報を探してください。見つかった項目は「この内容で合っていますか？」と確認し、不明・未記載の項目だけ質問してください。

**フォルダが見つからなかった場合:**
以下の7問を順番に質問してください。

質問項目：
1. あなたの名前（ニックネームでもOK）と、今やっている仕事・活動
2. あなたが今一番解決したい課題・悩み
3. 3年後にどんな状態になっていたいか（収入・働き方・生活など）
4. 今使っているSNSやビジネスツール（X・note・LINE等）
5. AIに一番やってほしいこと（例：タスク管理・投稿生成・情報整理）
6. 絶対にAIにやってほしくないこと・注意してほしいこと
7. あなたのビジネスの「核心的な強み」を一言で言うと

全項目が揃ったら、回答を整理して `./03_私について/my_profile.md` に書き込んでください。

my_profile.mdの形式：
```markdown
# 私のプロフィール
## 基本情報
- 名前：[回答]
- 活動：[回答]

## 現在の課題
[回答]

## 3年後のビジョン
[回答]

## 使用ツール・SNS
[回答]

## AIへの期待
[回答]

## AIへの制約・注意
[回答]

## 強み
[回答]
```

---

## Step 4: CLAUDE.md を作成する（グローバル）【共通】

~/.claude/CLAUDE.md を作成してください。
【重要】既存のファイルがある場合は上書きせず、末尾に追記する形にしてください。

以下の内容をそのまま書き込んでください。
[あなたの名前] の部分はStep3で聞いた名前に置き換えてください。
[AI名] の部分はあなたの好きな名前を入れてください（例: レイ、ハル、Aiなど）。

```markdown
## [AI名] — [あなたの名前]専用AIビジネスパートナー

- このClaudeは**[AI名]**として動作する（オーナー: [あなたの名前]）
- ミッション: **Claudeが作業を担い、[あなたの名前]は承認のみ**。手間最小化・自動化を最優先
- プロフィール参照: `./03_私について/my_profile.md`（Claude Codeの作業フォルダ基準）

---

## 行動原則

- **削除禁止** → 必ず `00_ゴミ箱/` に移動
- 不可逆操作（外部公開・決済・外部API送信）は確認なしに実行しない
- secrets/APIキー → コードに書かない・環境変数使用（.envを参照）
- .envのパス: `./02_設定/.env`（作業フォルダ基準）

---

## 自律実行ルール（毎回言わなくていい）

- **GREEN（ファイル操作・調査・生成・コード）** → 確認なしで即実行
- **YELLOW（外部サービス初回連携・設定変更）** → 実行前に1行報告してから進む
- **RED（支払い・課金・外部公開・契約・クライアント最終送信）** → 必ず止まって承認を待つ

---

## 一気通貫実行モード

以下のトリガーで自動発動：
- 「終わったら教えて」→ 全タスク完了まで無確認で連続実行。完了後に一括報告のみ
- タスクが番号付きリストで渡された → リスト末尾まで止まらず実行
- 「承認はすべてします」「確認不要」→ RED以外は一切止まらない

止まる唯一の条件: RED該当操作 / 「止めて」「待って」と言った時

完了報告フォーマット：
✅ 完了（[タスク数]件）
━━━━━━━━━━━━
✅ [タスク1] — 完了
⚠️ [タスク3] — スキップ（理由: ○○）
🔴 [タスク4] — 要承認（RED該当: ○○）
━━━━━━━━━━━━

---

## ナレッジベース — トリガーワード

| 言葉 | 動作 |
|---|---|
| 「タスク見せて」「やること」「進捗」 | MASTER_TASKS.mdを読んで現状報告 |
| 「全部やって」「片付けて」 | MASTER_TASKSのREDを除く全タスクを自律実行 |
| 「クリップ」+ 何か | `04_ナレッジ/切り抜き/` にMarkdownで保存 |
| URL貼るだけ | 記事取得 → `04_ナレッジ/切り抜き/` に自動保存 |
| 「まとめて」 | `04_ナレッジ/切り抜き/` の未整理素材 → `04_ナレッジ/情報源/` にWiki化 |
| 「〇〇を開いて」 | openコマンドで該当ファイル/フォルダを開く |
| 「AppLaudからタスク抽出」「AppLaudのタスクをMASTERに入れて」 | `python3 ./AppLaud/script/extract_tasks.py` を実行してMASTER_TASKS.mdを更新 |
| 「メモリ見せて」「記憶一覧」 | `~/.claude/projects/[カレントプロジェクトハッシュ]/memory/MEMORY.md` を読んで一覧表示 |
| 「〇〇を覚えておいて」「〇〇を記憶して」 | memoryフォルダに適切なタイプで保存し、MEMORY.mdに追記 |
| 「〇〇を忘れて」 | 該当memoryファイルを削除またはMEMORY.mdから除去 |

---

## memoryシステム — 永続記憶

Claude Codeには会話をまたいで記憶を保持する仕組みがある。
以下のルールでmemoryを読み書きすること。

### memoryの保存場所

`~/.claude/projects/[プロジェクトハッシュ]/memory/` に保存する。
プロジェクトハッシュは現在の作業ディレクトリから自動決定される。
- Mac例: `/Users/username/Projects/MyCourse` → `-Users-username-Projects-MyCourse`
- Windows例: `J:\GoogleApp\Claudecode` → `J--GoogleApp-Claudecode`

### memoryファイルの形式

```
---
name: short-kebab-case-slug
description: 一行説明（MEMORY.mdのインデックスに使う）
metadata:
  type: user | feedback | project | reference
---

本文（ルール・事実・理由・適用条件を書く）
```

### memoryの4タイプ

- **user**: ユーザーの役職・目標・知識レベル・好み
- **feedback**: 「こうしてほしい」「これはやめて」などの行動指針
- **project**: 進行中の案件・締め切り・決定事項
- **reference**: 外部システム・リソースへのポインタ

### MEMORY.md（インデックス）

`memory/MEMORY.md` に全memoryの一覧を管理する。200行以内に収める。
形式: `- [タイトル](ファイル名.md) — 一行フック`

### memoryを書くべきタイミング

- ユーザーに「覚えておいて」と言われた時
- ユーザーが好みや制約を明示した時（「〇〇はやめて」「〇〇がいい」）
- プロジェクトの重要な決定・締め切りを聞いた時
- 同じ間違いを繰り返さないための教訓が生まれた時

### 保存手順（2ステップ）

1. `memory/[スラッグ].md` をフロントマター付きで書き込む
2. `memory/MEMORY.md` の該当カテゴリに1行追記する

---

## Chatwork API 設計ルール（全スクリプト共通・永続）

新規・既存を問わず、Chatworkを扱うスクリプトは必ずこの設計に従う：

| 操作 | 使うトークン | 変数名 |
|---|---|---|
| 読み取り（GET） | メインアカウント | `CW_TOKEN` |
| 送信・通知（POST） | 通知用アカウント | `CW_NOTIFY_TOKEN` |

- `.env` から読み込む（ハードコード禁止）
- 送信時は必ず `CW_NOTIFY_TOKEN` を使う

---

## MyContextシステム全体フロー

```
① ボイスレコーダーで録音
↓ ② PCに繋ぐ
↓ ③ watch_usb.py が自動検知 → 音声ファイルを取り込み → 文字起こし・要約
↓ ④ ./05_日記/YYYY-MM-DD.md に今日の日報生成（pipeline.py）
↓ ⑤ 「AppLaudからタスク抽出」と言うとMASTER_TASKS.mdに反映
↓ ⑥ Claude Code起動（このCLAUDE.mdが自動読み込み）
↓ ⑦ 「今日の私の状況を教えて」と聞く
```
```

---

## Step 5: hooks スクリプトを作成する【共通】

### 5-1: ~/.claude/hooks/ フォルダを作成する

### 5-2: ~/.claude/hooks/block-api-key-output.py を作成する

```python
#!/usr/bin/env python3
import sys
import json
import re

API_KEY_PATTERNS = [
    r'sk-ant-api\d{2}-[A-Za-z0-9_-]{93}',
    r'sk-proj-[A-Za-z0-9_-]{80,}',
    r'AIzaSy[A-Za-z0-9_-]{33}',
    r'nvapi-[A-Za-z0-9_-]{40,}',
    r'ghp_[A-Za-z0-9]{36}',
    r'Bearer [A-Za-z0-9%+/]{40,}',
]

def contains_api_key(text):
    for pattern in API_KEY_PATTERNS:
        if re.search(pattern, text):
            return True
    return False

def main():
    try:
        data = json.loads(sys.stdin.read())
    except Exception:
        sys.exit(0)
    tool_input = data.get("tool_input", {})
    check_text = json.dumps(tool_input, ensure_ascii=False)
    if contains_api_key(check_text):
        print(json.dumps({
            "decision": "block",
            "reason": "⛔ APIキーが出力に含まれています。.envファイルを直接参照してください。"
        }, ensure_ascii=False))
        sys.exit(2)
    sys.exit(0)

if __name__ == "__main__":
    main()
```

### 5-3: ~/.claude/hooks/detect-secrets.py を作成する

```python
#!/usr/bin/env python3
import sys
import json
import re

SECRET_PATTERNS = [
    (r'(?i)(api[_-]?key|apikey)\s*[=:]\s*["\']?[A-Za-z0-9\-_]{20,}', "APIキー"),
    (r'(?i)(secret[_-]?key|secret)\s*[=:]\s*["\']?[A-Za-z0-9\-_]{20,}', "シークレットキー"),
    (r'(?i)(access[_-]?token|auth[_-]?token)\s*[=:]\s*["\']?[A-Za-z0-9\-_\.]{20,}', "アクセストークン"),
    (r'(?i)(password|passwd|pwd)\s*[=:]\s*["\']?[^\s"\']{8,}', "パスワード"),
    (r'sk-[A-Za-z0-9]{40,}', "OpenAI APIキー"),
    (r'sk-ant-[A-Za-z0-9\-_]{40,}', "Anthropic APIキー"),
    (r'AIza[A-Za-z0-9\-_]{35}', "Google APIキー"),
    (r'AKIA[A-Za-z0-9]{16}', "AWS Access Key ID"),
]

SAFE_FILE_PATTERNS = [r'\.env\.example', r'\.env\.sample', r'README\.md$', r'test[s]?/', r'detect-secrets\.py']

def is_safe_file(file_path):
    for pattern in SAFE_FILE_PATTERNS:
        if re.search(pattern, file_path, re.IGNORECASE):
            return True
    return False

def main():
    try:
        data = json.loads(sys.stdin.read())
    except Exception:
        sys.exit(0)
    tool_name = data.get("tool_name", "")
    tool_input = data.get("tool_input", {})
    if tool_name not in ("Write", "Edit"):
        sys.exit(0)
    file_path = tool_input.get("file_path", "")
    if is_safe_file(file_path) or file_path.endswith(".env"):
        sys.exit(0)
    content = tool_input.get("content", "") if tool_name == "Write" else tool_input.get("new_string", "")
    findings = []
    for pattern, name in SECRET_PATTERNS:
        if re.search(pattern, content):
            findings.append(name)
    if findings:
        print(json.dumps({
            "decision": "block",
            "reason": f"シークレット漏洩の可能性: {', '.join(findings)}\nAPIキーは.envファイルに保存してください。"
        }))
        sys.exit(2)
    sys.exit(0)

if __name__ == "__main__":
    main()
```

### 5-4: ~/.claude/hooks/user-prompt-save.py を作成する【共通・Mac/Windows同一】

```python
#!/usr/bin/env python3
import sys
import json
from datetime import datetime
from pathlib import Path

def main():
    try:
        data = json.loads(sys.stdin.read())
    except Exception:
        sys.exit(0)

    message = data.get("prompt", "") or data.get("message", "")
    if not message:
        sys.exit(0)

    cwd = data.get("cwd", "")
    if cwd:
        save_dir = Path(cwd) / "05_日記" / "チャットログ"
    else:
        save_dir = Path.home() / ".claude" / "chat_logs"

    save_dir.mkdir(parents=True, exist_ok=True)

    today = datetime.now().strftime("%Y-%m-%d")
    now = datetime.now().strftime("%H:%M:%S")

    log_file = save_dir / f"{today}_chat.md"
    if not log_file.exists():
        log_file.write_text(f"# チャットログ — {today}\n", encoding="utf-8")

    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"\n## {now}\n\n{str(message)[:2000]}\n\n---\n")

if __name__ == "__main__":
    main()
```

> ▶ **Mac のみ**: `chmod +x ~/.claude/hooks/user-prompt-save.py` を実行してください。

---

## Step 6: ~/.claude/settings.json を作成する（hooks有効化）【共通】

【重要】既存のsettings.jsonがある場合は上書きせず、"hooks"キーだけ追記・マージしてください。

```json
{
  "permissions": {
    "defaultMode": "acceptEdits"
  },
  "hooks": {
    "UserPromptSubmit": [
      {
        "type": "command",
        "command": "python3 ~/.claude/hooks/user-prompt-save.py",
        "timeout": 10
      }
    ],
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "python3 ~/.claude/hooks/block-api-key-output.py",
            "timeout": 5
          }
        ]
      },
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "python3 ~/.claude/hooks/detect-secrets.py",
            "timeout": 5
          }
        ]
      }
    ],
    "Stop": [
      {
        "type": "command",
        "command": "python3 ~/.claude/auto-save-context.py",
        "timeout": 30
      }
    ]
  }
}
```

---

## Step 7: auto-save-context.py を作成する【共通】

~/.claude/auto-save-context.py を作成してください。

```python
#!/usr/bin/env python3
"""セッション終了時にチャット履歴をMarkdownで自動保存する"""

import sys
import json
import os
from datetime import datetime
from pathlib import Path

def load_hook_input():
    try:
        return json.loads(sys.stdin.read())
    except Exception:
        return {}

def find_session_file(session_id):
    search_dirs = [Path.home() / ".claude" / "projects", Path.home() / ".claude" / "sessions"]
    for base in search_dirs:
        if not base.exists():
            continue
        for f in base.rglob("*.jsonl"):
            if session_id and session_id in f.name:
                return f
        files = sorted(base.rglob("*.jsonl"), key=lambda x: x.stat().st_mtime, reverse=True)
        if files:
            return files[0]
    return None

def parse_session(jsonl_path):
    messages = []
    try:
        with open(jsonl_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                    if obj.get("type") not in ("user", "assistant"):
                        continue
                    role = obj.get("type", "")
                    msg = obj.get("message", {})
                    content = msg.get("content", "")
                    if isinstance(content, list):
                        texts = [b.get("text", "") for b in content if isinstance(b, dict) and b.get("type") == "text"]
                        content = "\n".join(texts)
                    if content:
                        messages.append({"role": role, "content": str(content)[:3000]})
                except Exception:
                    continue
    except Exception:
        pass
    return messages

def main():
    hook_data = load_hook_input()
    session_id = hook_data.get("session_id", "unknown")
    project_cwd = hook_data.get("cwd", "")
    transcript_path = hook_data.get("transcript_path", "")

    if transcript_path and Path(transcript_path).exists():
        jsonl_path = Path(transcript_path)
    else:
        jsonl_path = find_session_file(session_id)

    if not jsonl_path:
        return

    messages = parse_session(jsonl_path)
    if not messages:
        return

    if project_cwd:
        save_dir = Path(project_cwd) / "05_日記" / "チャットログ"
    else:
        save_dir = Path.home() / ".claude" / "chat_logs"

    save_dir.mkdir(parents=True, exist_ok=True)

    date_str = datetime.now().strftime("%Y-%m-%d")
    sid_short = str(session_id)[:8]
    save_path = save_dir / f"{date_str}_{sid_short}.md"

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = [f"# チャット履歴\n\n- **保存日時**: {now}\n- **メッセージ数**: {len(messages)}\n\n---\n"]
    for msg in messages:
        label = "**私**" if msg["role"] == "user" else "**Claude**"
        lines.append(f"### {label}\n\n{msg['content']}\n\n---\n")

    with open(save_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"[auto-save] 保存完了: {save_path} ({len(messages)}件)", file=sys.stderr)

if __name__ == "__main__":
    main()
```

---

## Step 8: AppLaud をセットアップする【共通】

作業フォルダ内に AppLaud をクローンします（Mac/Windows両対応のフォーク版）：

> ▶ **Mac のみ**:
> ```bash
> git clone https://github.com/tonsuke1003-wq/AppLaud.git ./AppLaud
> pip3 install -r ./AppLaud/requirements.txt
> ```
> mp3/m4a処理に ffmpeg が必要です（未インストールの場合: `brew install ffmpeg`）

> ▶ **Windows のみ**:
> ```powershell
> git clone https://github.com/tonsuke1003-wq/AppLaud.git ./AppLaud
> pip install -r .\AppLaud\requirements.txt
> ```
> mp3/m4a処理に ffmpeg が必要です（[ffmpeg.org](https://ffmpeg.org/download.html) からインストールし PATH へ追加）

次に `./AppLaud/script/config.py` を開いて設定を確認してください：

```python
# ボイスレコーダーのドライブ/ボリューム（空文字列で全リムーバブルドライブを対象）
# Mac例: "/Volumes/IC RECORDER"  Windows例: "E:\\"
RECORDER_DRIVE = ""

# レコーダー内の音声ファイルサブディレクトリ（例: "RECORD" または ""）
VOICE_FILES_SUBDIR = "RECORD"
```

> APIキー（`GEMINI_API_KEY`）は `./02_設定/.env` から自動読み込みされます。`config.py` に直接書かないでください。

USB監視を起動するには：

> ▶ **Mac のみ**: `python3 ./AppLaud/script/watch_usb.py`

> ▶ **Windows のみ**: `python .\AppLaud\script\watch_usb.py`

ボイスレコーダーを接続すると自動で処理が開始されます（Ctrl+C で停止）。

手動実行（接続済みドライブを即時処理）：

> ▶ **Mac のみ**: `python3 ./AppLaud/script/watch_usb.py --once`

> ▶ **Windows のみ**: `python .\AppLaud\script\watch_usb.py --once`

**（上級）ログイン時に自動起動する場合：**

> ▶ **Mac のみ**: launchd で設定します。

```bash
WORK_DIR=$(pwd)
PYTHON_PATH=$(which python3)

cat > ~/Library/LaunchAgents/com.mycontext.applaud.plist << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key><string>com.mycontext.applaud</string>
    <key>ProgramArguments</key>
    <array>
        <string>${PYTHON_PATH}</string>
        <string>${WORK_DIR}/AppLaud/script/watch_usb.py</string>
    </array>
    <key>RunAtLoad</key><true/>
    <key>StandardOutPath</key><string>/tmp/applaud.log</string>
    <key>StandardErrorPath</key><string>/tmp/applaud-err.log</string>
</dict>
</plist>
EOF

launchctl load ~/Library/LaunchAgents/com.mycontext.applaud.plist
echo "✅ launchd に登録しました"
```

> ▶ **Windows のみ**: タスクスケジューラーで設定します。PowerShell を**管理者権限**で実行：

```powershell
$workDir = (Get-Location).Path
$scriptPath = "$workDir\AppLaud\script\watch_usb.py"
$pythonPath = (Get-Command python -ErrorAction SilentlyContinue)?.Source
if (-not $pythonPath) { $pythonPath = (Get-Command python3).Source }

schtasks /create `
  /tn "AppLaud\WatchUSB" `
  /tr "`"$pythonPath`" `"$scriptPath`"" `
  /sc ONLOGON `
  /ru "$env:USERNAME" /f

Write-Host "✅ タスクスケジューラーに登録しました"
```

---

## Step 9: pipeline.py を作成する【共通】

`./02_設定/pipeline.py` を作成してください。

```python
#!/usr/bin/env python3
"""
MyContext pipeline.py
AppLaudの出力（./06_AppLaud/）を読み取り、
今日の日報ファイル（./05_日記/YYYY-MM-DD.md）を生成する。
"""

import os
import glob
from datetime import datetime
from pathlib import Path

# スクリプト位置（02_設定/）の1つ上がプロジェクトルート
BASE_DIR = Path(__file__).parent.parent

def _load_env(path: Path):
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, _, v = line.partition("=")
                os.environ.setdefault(k.strip(), v.strip())

_load_env(BASE_DIR / "02_設定" / ".env")

APPLAUD_DIR = BASE_DIR / "06_AppLaud"
JOURNAL_DIR = BASE_DIR / "05_日記"

def get_todays_applaud():
    today = datetime.now().strftime("%Y-%m-%d")
    pattern = str(APPLAUD_DIR / f"{today}*.md")
    files = sorted(glob.glob(pattern))
    return files

def build_daily_journal(applaud_files):
    today = datetime.now().strftime("%Y-%m-%d")
    now = datetime.now().strftime("%H:%M")
    lines = [f"# {today} 日報\n\n**更新**: {now}\n\n---\n"]
    if applaud_files:
        lines.append("## 音声メモ（AppLaud）\n")
        for f in applaud_files:
            content = Path(f).read_text(encoding="utf-8")
            lines.append(f"### {Path(f).name}\n\n{content}\n\n---\n")
    else:
        lines.append("## 音声メモ\n\n（本日の音声メモなし）\n\n---\n")
    lines.append("## 今日のタスク\n\n（Claude Codeに「今日の私の状況を教えて」と聞いて確認）\n")
    return "\n".join(lines)

def main():
    JOURNAL_DIR.mkdir(parents=True, exist_ok=True)
    today = datetime.now().strftime("%Y-%m-%d")
    output_path = JOURNAL_DIR / f"{today}.md"
    applaud_files = get_todays_applaud()
    print(f"AppLaudファイル: {len(applaud_files)}件")
    md = build_daily_journal(applaud_files)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(md)
    print(f"✅ 日報を作成しました: {output_path}")

if __name__ == "__main__":
    main()
```

---

## Step 10: MASTER_TASKS.md と memory システムを作成する【共通】

### 10-1: MASTER_TASKS.md を作成する

`./07_タスク/MASTER_TASKS.md` を作成してください。

```markdown
# MASTER_TASKS.md — タスク管理

> ルール: タスクは必ずこのファイルに記録する。完了したら ✅ をつける。

---

## 🔴 優先度A（今週中）

| # | タスク | 期限 | 状態 |
|---|---|---|---|
| 1 | MyContextセットアップ完了 | 本日 | 🔄 進行中 |

---

## 🟡 優先度B（今月中）

| # | タスク | 期限 | 状態 |
|---|---|---|---|
|   |   |   |   |

---

## 🟢 優先度C（いつか）

| # | タスク | 期限 | 状態 |
|---|---|---|---|
|   |   |   |   |

---

## ✅ 完了済み

|   | タスク | 完了日 |
|---|---|---|
|   |   |   |

---

## ルール

- タスクは自然言語で追加・完了を伝えるだけで[AI名]が自動反映する
- AppLaud音声メモからもタスクを自動抽出できる（「AppLaudからタスク抽出」と言う）
- 期限が近いタスクは朝のブリーフィングで通知される
```

### 10-2: memory フォルダのパスを確認する

以下のPythonスクリプトを実行して、正しいパスを調べてください：

```python
import os
import re
import platform
from pathlib import Path

projects_dir = Path.home() / ".claude" / "projects"
cwd = str(Path.cwd())

if platform.system() == "Windows":
    # J:\GoogleApp\Claudecode → J--GoogleApp-Claudecode
    cwd_hash = re.sub(r'[:\\/]+', '-', cwd).strip('-')
else:
    # /Users/username/Projects/MyCourse → -Users-username-Projects-MyCourse
    cwd_hash = cwd.replace('/', '-')

memory_path = projects_dir / cwd_hash / "memory"

print(f"OS: {platform.system()}")
print(f"現在の作業フォルダ: {cwd}")
print(f"推定 memoryパス: {memory_path}")
print()
print("=== ~/.claude/projects/ 内のフォルダ一覧（最近使用順）===")
if projects_dir.exists():
    dirs = sorted(
        [d for d in projects_dir.iterdir() if d.is_dir()],
        key=lambda x: x.stat().st_mtime, reverse=True
    )
    for d in dirs[:10]:
        print(f"  {d.name}")
```

次に、出力されたパスにmemoryフォルダを作成してください。

### 10-3: MEMORY.md（インデックスファイル）を作成する

```markdown
# MEMORY INDEX

> このファイルのリンク先ファイルを自動で読みに行かないこと。必要な時だけ個別に Read する。

## ユーザー情報

- [プロフィール](user_profile.md) — ユーザーの基本情報・目標・好み

## フィードバック・行動ルール

（ここにfeedbackタイプのmemoryを追記していく）

## 進行中プロジェクト

（ここにprojectタイプのmemoryを追記していく）

## 参照先・外部リソース

（ここにreferenceタイプのmemoryを追記していく）
```

### 10-4: 最初のmemoryファイルを作成する

`user_profile.md`（MEMORY.mdと同じフォルダ内）を作成してください。

```markdown
---
name: user-profile
description: ユーザーの基本情報・目標・強み・AIへの期待と制約
metadata:
  type: user
---

# ユーザープロフィール

（./03_私について/my_profile.md の内容をここに要約して転記）
```

---

## Step 11: AppLaud タスク抽出スクリプトを追加する【共通】

`./AppLaud/script/extract_tasks.py` を作成してください。

```python
#!/usr/bin/env python3
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

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash-preview:generateContent?key={api_key}"
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
```

動作確認：

> ▶ **Mac のみ**: `python3 ./AppLaud/script/extract_tasks.py`

> ▶ **Windows のみ**: `python .\AppLaud\script\extract_tasks.py`

---

## Step 12: Chatwork 朝ブリーフィング設定

### 12-1: .envにChatworkのキーを追加する【共通】

`./02_設定/.env` を開いて、以下の3行を追加してください：

```
CW_TOKEN=
CW_NOTIFY_TOKEN=
CW_TARGET_ROOM=
```

### 12-2: chatwork-daily-digest.py を作成する【共通】

`./02_設定/chatwork-daily-digest.py` を作成してください。

```python
#!/usr/bin/env python3
"""
chatwork-daily-digest.py — 毎朝5:00に自動実行
1. Chatwork全ルームの24時間メッセージを収集
2. MASTER_TASKS.md + 直近日記 を参照
3. Gemini でブリーフィングを生成
4. 指定ルームに送信
"""

import urllib.request
import urllib.parse
import json
import time
import sys
import os
from datetime import datetime
from pathlib import Path

def _load_env(path: Path) -> dict:
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

BASE_DIR   = Path(__file__).parent.parent
ENV_PATH   = BASE_DIR / "02_設定" / ".env"
_ENV       = _load_env(ENV_PATH)

CW_TOKEN        = _ENV.get("CW_TOKEN", "")        or os.environ.get("CW_TOKEN", "")
CW_NOTIFY_TOKEN = _ENV.get("CW_NOTIFY_TOKEN", "") or os.environ.get("CW_NOTIFY_TOKEN", "") or CW_TOKEN
TARGET_ROOM     = _ENV.get("CW_TARGET_ROOM", "")  or os.environ.get("CW_TARGET_ROOM", "")
GEMINI_API_KEY  = _ENV.get("GEMINI_API_KEY", "")  or os.environ.get("GEMINI_API_KEY", "")
GEMINI_URL      = "https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash-preview:generateContent"

MASTER_TASKS = BASE_DIR / "07_タスク" / "MASTER_TASKS.md"
JOURNAL_DIR  = BASE_DIR / "05_日記"

CW_HEADERS        = {"X-ChatWorkToken": CW_TOKEN}
CW_NOTIFY_HEADERS = {"X-ChatWorkToken": CW_NOTIFY_TOKEN}
SINCE_SEC = 86400

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}", flush=True)

def cw_get(path):
    req = urllib.request.Request(f"https://api.chatwork.com/v2{path}", headers=CW_HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=20) as res:
            return json.load(res)
    except Exception as e:
        log(f"  API error {path}: {e}")
        return None

def cw_post_message(room_id, body):
    data = urllib.parse.urlencode({"body": body}).encode()
    req = urllib.request.Request(
        f"https://api.chatwork.com/v2/rooms/{room_id}/messages",
        data=data, headers=CW_NOTIFY_HEADERS, method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as res:
            return json.load(res)
    except Exception as e:
        log(f"  送信エラー: {e}")
        return None

def get_active_rooms():
    rooms = cw_get("/rooms")
    if not rooms:
        return []
    since = int(time.time()) - SINCE_SEC
    active = [r for r in rooms if r.get("last_update_time", 0) >= since]
    active.sort(key=lambda r: r.get("last_update_time", 0), reverse=True)
    return active

def get_room_messages(room_id):
    msgs = cw_get(f"/rooms/{room_id}/messages?force=1")
    if not msgs:
        return []
    since = int(time.time()) - SINCE_SEC
    return [m for m in msgs if m.get("send_time", 0) >= since]

def format_messages(room_name, messages):
    if not messages:
        return ""
    lines = [f"\n【{room_name}】"]
    for m in messages[-10:]:
        sender = m.get("account", {}).get("name", "?")
        body = m.get("body", "").replace("\n", " ").strip()[:100]
        if body:
            lines.append(f"  {sender}: {body}")
    return "\n".join(lines)

def read_master_tasks():
    try:
        return MASTER_TASKS.read_text(encoding="utf-8", errors="ignore")[:3000]
    except Exception:
        return "（MASTER_TASKS.mdが見つかりません）"

def read_recent_journals(n=2):
    if not JOURNAL_DIR.exists():
        return ""
    try:
        journals = sorted(JOURNAL_DIR.glob("*.md"), reverse=True)
    except Exception:
        return ""
    texts = []
    for j in journals[:n]:
        try:
            texts.append(f"=== {j.stem} ===\n{j.read_text(encoding='utf-8', errors='ignore')[:1500]}")
        except Exception:
            continue
    return "\n\n".join(texts)

def generate_briefing(chatwork_summary, master_tasks, journals):
    today = datetime.now().strftime("%Y年%m月%d日（%A）")
    prompt = f"""あなたは専属のAIアシスタントです。今日は{today}です。

## 昨日〜今日のChatworkメッセージサマリー
{chatwork_summary[:3000]}

## MASTER_TASKS
{master_tasks}

## 直近の日記
{journals[:1500]}

以下のChatworkマークアップ形式で朝のブリーフィングを作成してください。Markdown記法は使わないこと。

[info][title]🌅 {today} 朝のブリーフィング[/title][/info]
[info][title]📌 今日やるべきタスク[/title]（MASTER_TASKSから列挙）[/info]
[info][title]💬 昨日のChatwork要約[/title]（重要なやりとり・返信必要なものを箇条書き）[/info]
[info][title]⚠️ 要対応・期限あり[/title]（期限が近いもの）[/info]
[info][title]📝 今日のひとこと[/title]（励ましや気づきを1〜2文）[/info]"""

    payload = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"maxOutputTokens": 4096, "temperature": 0.7},
    }, ensure_ascii=False).encode("utf-8")

    url = f"{GEMINI_URL}?key={GEMINI_API_KEY}"
    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=60) as res:
            data = json.load(res)
            return data["candidates"][0]["content"]["parts"][0]["text"].strip()
    except Exception as e:
        log(f"❌ Gemini APIエラー: {e}")
        return None

def main():
    if not TARGET_ROOM:
        log("❌ CW_TARGET_ROOMが.envに設定されていません")
        sys.exit(1)
    if not GEMINI_API_KEY:
        log("❌ GEMINI_API_KEYが.envに設定されていません")
        sys.exit(1)

    log("=== 朝のブリーフィング生成開始 ===")
    active_rooms = get_active_rooms()
    log(f"アクティブなルーム: {len(active_rooms)}件")

    chatwork_sections = []
    for room in active_rooms[:20]:
        room_id = room["room_id"]
        messages = get_room_messages(room_id)
        if messages:
            chatwork_sections.append(format_messages(room.get("name", str(room_id)), messages))
        time.sleep(0.2)

    chatwork_summary = "\n".join(chatwork_sections) if chatwork_sections else "（メッセージなし）"
    master_tasks = read_master_tasks()
    journals = read_recent_journals(3)

    log("Gemini でブリーフィング生成中...")
    briefing = generate_briefing(chatwork_summary, master_tasks, journals)
    if not briefing:
        log("❌ ブリーフィング生成失敗")
        sys.exit(1)

    log(f"Chatwork room={TARGET_ROOM} に送信中...")
    result = cw_post_message(TARGET_ROOM, briefing)
    if result:
        log(f"✅ 送信完了 (message_id: {result.get('message_id', '?')})")
    else:
        log("❌ 送信失敗")
        sys.exit(1)

if __name__ == "__main__":
    main()
```

### 12-3: 毎朝5:00に自動実行する設定

> ▶ **Mac のみ**: launchd で設定します。

```bash
WORK_DIR=$(pwd)
PYTHON_PATH=$(which python3)

cat > ~/Library/LaunchAgents/com.mycontext.chatwork-digest.plist << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key><string>com.mycontext.chatwork-digest</string>
    <key>ProgramArguments</key>
    <array>
        <string>${PYTHON_PATH}</string>
        <string>${WORK_DIR}/02_設定/chatwork-daily-digest.py</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key><integer>5</integer>
        <key>Minute</key><integer>0</integer>
    </dict>
    <key>StandardOutPath</key><string>/tmp/chatwork-digest.log</string>
    <key>StandardErrorPath</key><string>/tmp/chatwork-digest-err.log</string>
    <key>RunAtLoad</key><true/>
</dict>
</plist>
EOF

launchctl load ~/Library/LaunchAgents/com.mycontext.chatwork-digest.plist
echo "✅ launchd に登録しました（RunAtLoad=true: 起動時にも実行）"
```

手動テスト：
```bash
python3 ./02_設定/chatwork-daily-digest.py
```

---

> ▶ **Windows のみ**: Windowsタスクスケジューラーで設定します。

PowerShellを**管理者権限**で実行してください：

```powershell
$workDir    = (Get-Location).Path
$scriptPath = "$workDir\02_設定\chatwork-daily-digest.py"
$pythonPath = (Get-Command python -ErrorAction SilentlyContinue)?.Source
if (-not $pythonPath) { $pythonPath = (Get-Command python3).Source }

$action   = New-ScheduledTaskAction -Execute "`"$pythonPath`"" -Argument "`"$scriptPath`""
$trigger  = New-ScheduledTaskTrigger -Daily -At "05:00"
$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -ExecutionTimeLimit (New-TimeSpan -Minutes 30)

Register-ScheduledTask `
  -TaskName "MyContext\ChatworkDailyDigest" `
  -Action $action `
  -Trigger $trigger `
  -Settings $settings `
  -RunLevel Limited `
  -Force

Write-Host "✅ タスクスケジューラーに登録しました（PC起動後の遅延実行あり）"
```

手動テスト：
```powershell
python .\02_設定\chatwork-daily-digest.py
```

---

## Step 13: 動作確認

> ▶ **Mac のみ**: 以下のbashコマンドで確認してください。

```bash
ls ./                        # フォルダが全部あるか
ls ~/.claude/hooks/          # 3つのPythonスクリプトがあるか
cat ~/.claude/CLAUDE.md      # 名前・memoryシステムが入っているか
cat ./03_私について/my_profile.md
cat ./07_タスク/MASTER_TASKS.md
ls ~/.claude/projects/       # 作業フォルダに対応するプロジェクトフォルダがあるか
cat ./02_設定/.env            # 全4キーの行があるか（値は空でOK）
launchctl list | grep com.mycontext   # chatwork-digestジョブが登録されているか
```

---

> ▶ **Windows のみ**: 以下のPowerShellコマンドで確認してください。

```powershell
dir .\                       # フォルダが全部あるか
dir $HOME\.claude\hooks\     # 3つのPythonスクリプトがあるか
Get-Content $HOME\.claude\CLAUDE.md   # 名前・memoryシステムが入っているか
Get-Content .\03_私について\my_profile.md
Get-Content .\07_タスク\MASTER_TASKS.md
dir $HOME\.claude\projects\  # 作業フォルダに対応するプロジェクトフォルダがあるか
Get-Content .\02_設定\.env    # 全4キーの行があるか（値は空でOK）
schtasks /query /tn "MyContext\ChatworkDailyDigest"   # タスクが登録されているか
```

---

全部確認できたら「セットアップ完了です」と報告してください。