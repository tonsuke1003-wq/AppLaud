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
CW_TOKEN=
CW_NOTIFY_TOKEN=
CW_TARGET_ROOM=
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
| 「AppLaud確認して」「AppLaud動いてる？」「音声メモ確認」 | AppLaud処理済みログ確認・未処理ファイル確認・最新要約確認を実行して報告 |
| 「AppLaud手動実行」「音声を処理して」「録音を処理して」 | `./AppLaud/` 内の未処理ファイルを手動で処理 |
| 「AppLaud最新の要約見せて」「最後のAppLaud何の話だった？」 | `./06_AppLaud/` の最新MDファイルを読んで内容を報告 |
| 「AppLaudが止まってる」「音声処理が止まってる」 | `.tmp_chunks`確認→stale削除→再実行で自律復旧 |
| 「記事を知識にまとめて」「保存した記事を整理して」 | `python3 ./02_設定/vault-maintenance.py compile` を実行 |
| 「知識ページをチェックして」「ナレッジ古くなってない？」 | `python3 ./02_設定/vault-maintenance.py lint` を実行 |
| 「知識一覧更新して」「まとめ一覧を作り直して」 | `python3 ./02_設定/vault-maintenance.py index` を実行 |
| 「メモリ見せて」「記憶一覧」 | `~/.claude/projects/[カレントプロジェクトハッシュ]/memory/MEMORY.md` を読んで一覧表示 |
| 「〇〇を覚えておいて」「〇〇を記憶して」 | memoryフォルダに適切なタイプで保存し、MEMORY.mdに追記 |
| 「〇〇を忘れて」 | 該当memoryファイルを削除またはMEMORY.mdから除去 |

---

## サブエージェント ルーティング

「レビューして」「サブエージェントでチェックして」と言われたら、直前の作業に合わせて最適なエージェントを起動する。

| 直前の作業 | 起動するエージェント |
|---|---|
| Pythonコード | `python-reviewer` |
| TypeScript / JavaScriptコード | `typescript-reviewer` |
| その他コード・汎用 | `code-reviewer` |
| DB設計・SQLクエリ | `database-reviewer` |
| システム設計・技術選定 | `architect` |
| セキュリティ懸念あり | `security-reviewer` |

---

## アプリ・システム構築ルール（A→B→C）

「〇〇を作って」「〇〇を修正して」など構築・改修依頼が来た時は必ずA→B→Cの順で進める。

### ターンA（監査）— コード編集禁止
- 関連ファイルを読み、現状実装を把握する
- 仕様の各要件を「実装済み／一部実装／未実装／仕様ズレ」の4分類で判定する
- 各判定に根拠となるファイル名・関数名・行番号を必ず書く

### ターンB（計画）— コード編集禁止
- 未実装・仕様ズレ項目だけを対象に改修計画を書く
- 「対象ファイル・変更内容・確認方法」を明記する

### ターンC（実装）
- 前ターンの計画に載っている内容だけ実装する
- 実装後は要件チェックリストで自己監査する
- 未達項目があれば完了と書かず未達一覧を明示する

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
        "hooks": [
          {
            "type": "command",
            "command": "python3 ~/.claude/hooks/user-prompt-save.py",
            "timeout": 10
          }
        ]
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
        "hooks": [
          {
            "type": "command",
            "command": "python3 ~/.claude/auto-save-context.py 2>/dev/null || true",
            "timeout": 30,
            "async": true,
            "statusMessage": "チャット履歴を自動保存中..."
          }
        ]
      }
    ]
  }
}
```

> ▶ **Windows のみ**: すべての `command` パスを **フォワードスラッシュ（`/`）** で書いてください。バックスラッシュ（`\`）は JSON 内でエスケープ処理が壊れ、フックが動作しません。
>
> | Mac（そのまま） | Windows（要変更） |
> |---|---|
> | `python3 ~/.claude/hooks/user-prompt-save.py` | `python C:/Users/[ユーザー名]/.claude/hooks/user-prompt-save.py` |
> | `python3 ~/.claude/hooks/block-api-key-output.py` | `python C:/Users/[ユーザー名]/.claude/hooks/block-api-key-output.py` |
> | `python3 ~/.claude/hooks/detect-secrets.py` | `python C:/Users/[ユーザー名]/.claude/hooks/detect-secrets.py` |
> | `python3 ~/.claude/auto-save-context.py 2>/dev/null \|\| true` | `python C:/Users/[ユーザー名]/.claude/auto-save-context.py` |
>
> ※ `[ユーザー名]` は実際のWindowsユーザー名に置き換えてください（`echo %USERNAME%` で確認できます）。

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
$workDir    = (Get-Location).Path
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
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
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

## Step 10: vault-maintenance.py を作成する【共通】

ナレッジ管理スクリプトを作成します。「記事を知識にまとめて」などのトリガーワードでClaudeが自動実行します。

`./02_設定/vault-maintenance.py` を作成してください。

```python
#!/usr/bin/env python3
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
"""
vault-maintenance.py
04_ナレッジ/切り抜き/ のMarkdown記事をGemini APIでWiki知識ページに変換し、
04_ナレッジ/情報源/ に保存する。

使い方:
  python3 ./02_設定/vault-maintenance.py compile  # 切り抜き→情報源変換
  python3 ./02_設定/vault-maintenance.py lint     # 古い/重複ページを検出
  python3 ./02_設定/vault-maintenance.py index    # 情報源/_index.md を再生成
"""

import sys
import os
import json
import urllib.request
from pathlib import Path
from datetime import datetime, timezone

# スクリプト位置（02_設定/）の1つ上がプロジェクトルート
BASE_DIR  = Path(__file__).parent.parent
CLIPPINGS = BASE_DIR / "04_ナレッジ" / "切り抜き"
SOURCES   = BASE_DIR / "04_ナレッジ" / "情報源"
ENV_PATH  = BASE_DIR / "02_設定" / ".env"
DEFAULT_GEMINI_MODEL = "gemini-3-flash-preview"

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

def get_gemini_key() -> str:
    env = load_env(ENV_PATH)
    return env.get("GEMINI_API_KEY", "") or os.environ.get("GEMINI_API_KEY", "")

def gemini_generate(prompt: str, api_key: str, model: str = DEFAULT_GEMINI_MODEL) -> str:
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    payload = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"maxOutputTokens": 4096, "temperature": 0.3},
    }, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=60) as res:
            data = json.load(res)
            return data["candidates"][0]["content"]["parts"][0]["text"].strip()
    except Exception as e:
        print(f"  Gemini APIエラー: {e}", file=sys.stderr)
        return ""

def cmd_compile():
    api_key = get_gemini_key()
    if not api_key:
        print("❌ GEMINI_API_KEYが.envに設定されていません")
        print(f"   設定先: {ENV_PATH}")
        sys.exit(1)

    SOURCES.mkdir(parents=True, exist_ok=True)
    clips = sorted(CLIPPINGS.glob("*.md")) if CLIPPINGS.exists() else []

    if not clips:
        print(f"切り抜きにファイルが見つかりません: {CLIPPINGS}")
        return

    print(f"対象: {len(clips)}件")
    converted = 0

    for clip in clips:
        out_name = clip.stem + "_wiki.md"
        out_path = SOURCES / out_name
        if out_path.exists():
            print(f"  スキップ（既存）: {clip.name}")
            continue

        print(f"  変換中: {clip.name} → {out_name}")
        text = clip.read_text(encoding="utf-8", errors="ignore")

        prompt = f"""以下はWebページの切り抜き記事です。
この内容を「いつでも参照できる知識ページ（Wiki形式）」に変換してください。

【変換ルール】
- タイトルは「# 知識: [トピック名]」の形式
- 「## 要点」「## 詳細」「## 活用メモ」の3セクションで構成
- 時事的な内容（「今日は〜」「最近は〜」など）は削除し、恒久的な知識だけ残す
- 元記事のURLがあればfooterに「出典: [URL]」として記載
- 日本語で出力

【元記事】
{text[:4000]}
"""
        wiki = gemini_generate(prompt, api_key)
        if not wiki:
            print(f"    ⚠️ 変換失敗: {clip.name}")
            continue

        header = f"---\nsource: {clip.name}\ncreated: {datetime.now(timezone.utc).strftime('%Y-%m-%d')}\n---\n\n"
        out_path.write_text(header + wiki, encoding="utf-8")
        converted += 1

    print(f"\n✅ 変換完了: {converted}件 → {SOURCES}")

def cmd_lint():
    if not SOURCES.exists():
        print(f"情報源フォルダが存在しません: {SOURCES}")
        return

    pages = sorted(SOURCES.glob("*.md"))
    pages = [p for p in pages if p.name != "_index.md"]
    print(f"チェック対象: {len(pages)}件\n")

    issues = []
    now = datetime.now(timezone.utc)
    titles = {}

    for page in pages:
        try:
            text = page.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue

        for line in text.splitlines():
            if line.startswith("created:"):
                try:
                    created_str = line.split(":", 1)[1].strip()
                    created = datetime.fromisoformat(created_str).replace(tzinfo=timezone.utc)
                    age_days = (now - created).days
                    if age_days > 180:
                        issues.append(f"⏰ 古い ({age_days}日): {page.name}")
                except Exception:
                    pass

        for line in text.splitlines():
            if line.startswith("# "):
                title = line.lstrip("# ").strip()
                if title in titles:
                    issues.append(f"🔁 重複タイトル: {page.name} ← {titles[title]}")
                else:
                    titles[title] = page.name
                break

    if not issues:
        print("✅ 問題なし（古いページ・重複なし）")
    else:
        print("⚠️ 検出された問題:")
        for issue in issues:
            print(f"  {issue}")
        print(f"\n合計: {len(issues)}件")

def cmd_index():
    SOURCES.mkdir(parents=True, exist_ok=True)
    pages = sorted(SOURCES.glob("*.md"))
    pages = [p for p in pages if p.name != "_index.md"]

    lines = [
        "# ナレッジ インデックス\n",
        f"> 最終更新: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n",
        f"> 総ページ数: {len(pages)}\n",
        "\n---\n",
    ]

    for page in pages:
        try:
            text = page.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        title = page.stem
        desc = ""
        for line in text.splitlines():
            if line.startswith("# "):
                title = line.lstrip("# ").strip()
            if line.startswith("## 要点"):
                idx = text.find("## 要点")
                snippet_start = idx + len("## 要点")
                snippet = text[snippet_start:snippet_start + 100].strip()
                desc = snippet.split("\n")[0][:80]
                break
        lines.append(f"- [{title}]({page.name}) — {desc}\n")

    index_path = SOURCES / "_index.md"
    index_path.write_text("".join(lines), encoding="utf-8")
    print(f"✅ インデックス更新完了: {index_path} ({len(pages)}件)")

COMMANDS = {
    "compile": cmd_compile,
    "lint":    cmd_lint,
    "index":   cmd_index,
}

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in COMMANDS:
        print("使い方: python3 vault-maintenance.py [compile|lint|index]")
        print("  compile — 切り抜き/ の記事を情報源/ のWikiページに変換")
        print("  lint    — 情報源/ の古いページ・重複を検出")
        print("  index   — 情報源/_index.md を再生成")
        sys.exit(1)
    COMMANDS[sys.argv[1]]()
```

動作確認（APIキー未設定でもOK）：

> ▶ **Mac のみ**: `python3 ./02_設定/vault-maintenance.py index`

> ▶ **Windows のみ**: `python .\02_設定\vault-maintenance.py index`

---

## Step 11: MASTER_TASKS.md と memory システムを作成する【共通】

### 11-1: MASTER_TASKS.md を作成する

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

### 11-2: memory フォルダのパスを確認する

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

### 11-3: MEMORY.md（インデックスファイル）を作成する

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

### 11-4: 最初のmemoryファイルを作成する

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

## Step 12: AppLaud タスク抽出スクリプトを追加する【共通】

`./AppLaud/script/extract_tasks.py` を作成してください。

```python
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

## Step 13: Chatwork 朝ブリーフィング設定

> `.env` の4キーはStep 2で作成済みです。値をテキストエディタで入力してから先に進んでください。
> （`CW_TOKEN` / `CW_NOTIFY_TOKEN` / `CW_TARGET_ROOM` / `GEMINI_API_KEY`）

### 13-1: chatwork-daily-digest.py を作成する【共通】

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

### 13-2: 毎朝5:00に自動実行する設定

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

## Step 14: ダッシュボード・ランチャーを作成する

CLAUDE.mdビューア・ルール解説・アプリランチャー・スキル一覧・Claude起動ショートカットの5ファイルを作成します。

> **確認事項（作成前に答えてください）**
>
> 1. Step 4 で決めた「あなたの名前（ニックネーム）」は何ですか？
> 2. Step 4 で決めた「AI名」は何ですか？
>
> この2つの値を以下の `[あなたの名前]` と `[AI名]` のプレースホルダーに当てはめながら5ファイルを作成してください。

---

### 14-1: CLAUDE.md ビューア（claude_md_viewer.html）

`./claude_md_viewer.html` を以下の内容で作成してください。
`[あなたの名前]` と `[AI名]` は Step 4 で決めた値に置き換えてください。

```html
<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>CLAUDE.md ビューア — [あなたの名前]のAIシステム</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: 'Hiragino Sans', 'Noto Sans JP', sans-serif; background: #0d0d0d; color: #e8e8e8; min-height: 100vh; }
  header { background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); border-bottom: 1px solid #2a2a4a; padding: 24px 32px; }
  header h1 { font-size: 22px; font-weight: 700; color: #fff; }
  header p { font-size: 13px; color: #7a7aaa; margin-top: 4px; }
  .tab-bar { display: flex; background: #111; border-bottom: 1px solid #222; padding: 0 32px; }
  .tab-btn { padding: 14px 28px; font-size: 14px; font-weight: 600; color: #666; border: none; background: none; cursor: pointer; border-bottom: 3px solid transparent; transition: all 0.2s; }
  .tab-btn.active { color: #a0a0ff; border-bottom-color: #a0a0ff; }
  .container { max-width: 860px; margin: 0 auto; padding: 32px 24px; }
  .section { background: #111; border: 1px solid #222; border-radius: 12px; padding: 24px; margin-bottom: 16px; }
  .section-title { font-size: 15px; font-weight: 700; color: #e8e8e8; margin-bottom: 8px; }
  .section-desc { font-size: 13px; color: #888; line-height: 1.7; margin-bottom: 12px; }
  .rule-block { background: #0a0a0a; border-left: 3px solid #4a4aff; border-radius: 6px; padding: 12px 16px; font-size: 13px; color: #b0b0e8; line-height: 1.8; margin-top: 8px; }
  .badge { display: inline-block; font-size: 10px; font-weight: 700; letter-spacing: 1px; padding: 3px 10px; border-radius: 20px; margin-right: 8px; margin-bottom: 8px; }
  .badge-global { background: rgba(100,140,212,0.15); color: #6496D4; border: 1px solid rgba(100,140,212,0.3); }
</style>
</head>
<body>
<header>
  <h1>🧠 CLAUDE.md ビューア — [あなたの名前]のAIシステム</h1>
  <p>[AI名]（Claude Code）の動作を定義する設定ファイルの可視化</p>
</header>
<div class="tab-bar">
  <button class="tab-btn active">グローバル設定（~/.claude/CLAUDE.md）</button>
</div>
<div class="container">
  <div class="section">
    <div class="section-title">[AI名] — [あなたの名前]専用AIビジネスパートナー</div>
    <span class="badge badge-global">GLOBAL</span>
    <div class="section-desc">このCLAUDE.mdが[AI名]の「人格・基本ルール」を定義する。どのフォルダで起動しても常に読み込まれる。</div>
    <div class="rule-block">
      GREEN（ファイル操作・調査・生成・コード）→ 確認なしで即実行<br>
      YELLOW（外部サービス初回連携・設定変更）→ 実行前に1行報告してから進む<br>
      RED（支払い・課金承認・外部公開・契約）→ 必ず止まって確認を待つ
    </div>
  </div>
  <div class="section">
    <div class="section-title">一気通貫実行モード</div>
    <div class="section-desc">「終わったら教えて」「全部やって」「番号付きリスト」で自動発動。REDだけ止まる。</div>
  </div>
  <div class="section">
    <div class="section-title">ナレッジベース — トリガーワード</div>
    <div class="rule-block">
      「タスク見せて」→ MASTER_TASKS.mdを読んで報告<br>
      「全部やって」→ REDを除く全タスクを自律実行<br>
      「クリップ」→ 04_ナレッジ/切り抜き/ に保存<br>
      「まとめて」→ 切り抜き/ を 情報源/ にWiki化<br>
      「記事を知識にまとめて」→ vault-maintenance.py compile<br>
      URL貼るだけ → 自動取得・保存
    </div>
  </div>
  <div class="section">
    <div class="section-title">ターンA→B→C（アプリ・システム構築）</div>
    <div class="rule-block">
      A（監査）: 現状を把握・要件を分類。コード編集禁止<br>
      B（計画）: 未実装・仕様ズレのみ対象に計画。コード編集禁止<br>
      C（実装）: 計画通りに実装。スコープを勝手に広げない
    </div>
  </div>
</div>
<script>
  document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
    });
  });
</script>
</body>
</html>
```

---

### 14-2: CLAUDE.md ルール解説（claude_md_rules.html）

`./claude_md_rules.html` を以下の内容で作成してください。
`[あなたの名前]` と `[AI名]` は Step 4 で決めた値に置き換えてください。

```html
<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>CLAUDE.md ルール解説 — [あなたの名前]×[AI名]</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: 'Hiragino Kaku Gothic ProN', 'Noto Sans JP', sans-serif; background: #0f1117; color: #e2e8f0; line-height: 1.7; }
  .header { background: linear-gradient(135deg, #1a1a2e, #16213e); padding: 40px 32px; border-bottom: 1px solid #2a2a4a; }
  h1 { font-size: 24px; font-weight: 800; color: #fff; }
  .subtitle { font-size: 13px; color: #7a7aaa; margin-top: 6px; }
  .layout { display: flex; min-height: calc(100vh - 120px); }
  .sidebar { width: 220px; flex-shrink: 0; background: #0d0d14; border-right: 1px solid #1e1e30; padding: 24px 0; position: sticky; top: 0; height: 100vh; overflow-y: auto; }
  .sidebar-item { display: block; padding: 10px 20px; font-size: 13px; color: #666; cursor: pointer; border-left: 3px solid transparent; transition: all 0.2s; text-decoration: none; }
  .sidebar-item:hover, .sidebar-item.active { color: #a0a0ff; border-left-color: #a0a0ff; background: rgba(100,100,255,0.06); }
  .main { flex: 1; padding: 40px; max-width: 720px; }
  .section { margin-bottom: 48px; }
  .section-title { font-size: 18px; font-weight: 700; color: #e2e8f0; margin-bottom: 16px; padding-bottom: 12px; border-bottom: 1px solid #222; }
  .rule-card { background: #131825; border: 1px solid #1e2a3a; border-radius: 10px; padding: 20px; margin-bottom: 14px; }
  .rule-title { font-size: 14px; font-weight: 700; color: #a0c4ff; margin-bottom: 8px; }
  .rule-why { font-size: 12px; color: #64748b; line-height: 1.8; margin-bottom: 8px; }
  .original-block { background: #0a0f1a; border-left: 3px solid #4a6fa5; padding: 10px 14px; font-size: 12px; color: #7090b0; border-radius: 4px; font-family: monospace; }
  .file-badge { display: inline-block; font-size: 10px; font-weight: 700; padding: 2px 8px; border-radius: 12px; background: rgba(100,140,212,0.15); color: #6496D4; border: 1px solid rgba(100,140,212,0.3); margin-left: 8px; vertical-align: middle; }
</style>
</head>
<body>
<div class="header">
  <h1>CLAUDE.md ルール解説 — [あなたの名前] × [AI名]</h1>
  <p class="subtitle">各ルールの「なぜ」を解説するリファレンス</p>
</div>
<div class="layout">
  <nav class="sidebar">
    <a class="sidebar-item active" onclick="scrollToSection('green-yellow-red', this)">① GREEN/YELLOW/RED</a>
    <a class="sidebar-item" onclick="scrollToSection('one-shot', this)">② 一気通貫実行</a>
    <a class="sidebar-item" onclick="scrollToSection('triggers', this)">③ トリガーワード</a>
    <a class="sidebar-item" onclick="scrollToSection('turn-abc', this)">④ ターンA→B→C</a>
    <a class="sidebar-item" onclick="scrollToSection('never', this)">⑤ 絶対にやらせない原則</a>
  </nav>
  <main class="main">
    <div class="section" id="green-yellow-red">
      <div class="section-title">① GREEN / YELLOW / RED <span class="file-badge">グローバル</span></div>
      <div class="rule-card">
        <div class="rule-title">行動を3段階に分類してAIの自律性を制御する</div>
        <div class="rule-why">全ての操作にいちいち確認していたら効率が下がる。でも全部任せると取り消せない操作が起きる。GREEN/YELLOW/REDで「止まる場所だけ明示」することで、AIは迷わず動き続けられる。</div>
        <div class="original-block">GREEN → 確認なし即実行 / YELLOW → 1行報告して続行 / RED → 必ず止まって確認</div>
      </div>
    </div>
    <div class="section" id="one-shot">
      <div class="section-title">② 一気通貫実行モード <span class="file-badge">グローバル</span></div>
      <div class="rule-card">
        <div class="rule-title">「終わったら教えて」だけで全タスクを連続実行させる</div>
        <div class="rule-why">タスクごとに「次どうしますか？」と止まるAIは生産性を下げる。発動トリガーと停止条件を明示することで、人間は承認だけすれば済む状態を作る。</div>
        <div class="original-block">「終わったら教えて」「全部やって」「番号付きリスト」で自動発動。止まる唯一の条件: RED該当 / 「止めて」と言った時</div>
      </div>
    </div>
    <div class="section" id="triggers">
      <div class="section-title">③ トリガーワード <span class="file-badge">グローバル</span></div>
      <div class="rule-card">
        <div class="rule-title">コマンドより「言葉で動く」設計</div>
        <div class="rule-why">「タスク見せて」「まとめて」など自然な言葉でAIが動く設計にすることで、ツールを意識せず使える。コマンドを覚えるコストをゼロにする。</div>
        <div class="original-block">「タスク見せて」→ MASTER_TASKS確認 / URL貼るだけ → 自動クリップ / 「全部やって」→ 自律実行</div>
      </div>
    </div>
    <div class="section" id="turn-abc">
      <div class="section-title">④ ターンA→B→C <span class="file-badge">グローバル</span></div>
      <div class="rule-card">
        <div class="rule-title">実装前に必ず監査→計画を挟む</div>
        <div class="rule-why">AIは指示されると即コードを書きたがる。でも現状把握なしに書いたコードは既存の仕様とズレることが多い。AとBでコード編集を禁止することで「考えてから作る」を強制する。</div>
        <div class="original-block">A（監査）→ B（計画）→ C（実装）の順。AとBはコード編集禁止</div>
      </div>
    </div>
    <div class="section" id="never">
      <div class="section-title">⑤ 絶対にやらせない原則 <span class="file-badge">グローバル</span></div>
      <div class="rule-card">
        <div class="rule-title">人間が操作すべき場面をAIに任せない</div>
        <div class="rule-why">エラー修正・情報取得・代替手段の模索は全てAIが自律解決する。「貼り付けてください」「確認してください」は禁止。AIが詰まっても人間を巻き込まず、解決してから報告する。</div>
        <div class="original-block">エラー修正 / URL取得 / ツール代替策 → 全てAIが自律解決してから報告</div>
      </div>
    </div>
  </main>
</div>
<script>
  function scrollToSection(id, el) {
    document.getElementById(id).scrollIntoView({ behavior: 'smooth' });
    document.querySelectorAll('.sidebar-item').forEach(e => e.classList.remove('active'));
    el.classList.add('active');
  }
</script>
</body>
</html>
```

---

### 14-3: アプリ一覧ランチャー（app_launcher.html）

`./app_launcher.html` を以下の内容で作成してください。
`[あなたの名前]` と `[AI名]` は Step 4 で決めた値に置き換えてください。

```html
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>[あなたの名前] — アプリ一覧</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: sans-serif; background: #0F0F0F; color: #F0EDE8; min-height: 100vh; padding: 40px 20px; }
    .header { text-align: center; margin-bottom: 48px; }
    .header-badge { display: inline-block; background: linear-gradient(135deg, #D4726A, #B76E79); color: white; font-size: 11px; font-weight: 700; letter-spacing: 2px; padding: 6px 16px; border-radius: 20px; margin-bottom: 16px; }
    .header h1 { font-size: 28px; font-weight: 700; margin-bottom: 8px; }
    .header p { font-size: 13px; color: #7A7570; }
    .grid { max-width: 860px; margin: 0 auto; display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 16px; }
    .card { background: #1A1A1A; border: 1px solid #2A2A2A; border-radius: 16px; padding: 24px; transition: all 0.2s; }
    .card:hover { border-color: #444; transform: translateY(-2px); }
    .card-icon { font-size: 36px; margin-bottom: 14px; display: block; }
    .card-tag { display: inline-block; font-size: 10px; font-weight: 700; letter-spacing: 1.5px; padding: 3px 10px; border-radius: 20px; margin-bottom: 10px; }
    .tag-tool { background: rgba(100,140,212,0.15); color: #6496D4; border: 1px solid rgba(100,140,212,0.3); }
    .tag-local { background: rgba(160,100,200,0.15); color: #C87EE0; border: 1px solid rgba(160,100,200,0.3); }
    .card h2 { font-size: 16px; font-weight: 700; margin-bottom: 6px; }
    .card p { font-size: 12px; color: #7A7570; line-height: 1.7; margin-bottom: 20px; }
    .btn-open { display: inline-block; background: linear-gradient(135deg, #D4726A, #B76E79); color: white; text-decoration: none; padding: 10px 20px; border-radius: 30px; font-size: 13px; font-weight: 700; cursor: pointer; border: none; transition: all 0.2s; }
    .btn-open:hover { opacity: 0.85; }
    .card-claude { background: linear-gradient(135deg, #1A1A2E 0%, #16213E 100%); border-color: #2A2A4A; grid-column: 1 / -1; }
    .claude-inner { display: flex; align-items: center; gap: 24px; flex-wrap: wrap; }
    .claude-icon { font-size: 48px; flex-shrink: 0; }
    .claude-info { flex: 1; min-width: 200px; }
    .claude-info h2 { font-size: 18px; margin-bottom: 6px; }
    .claude-info p { margin-bottom: 0; }
    .cmd-box { background: #0A0A1A; border: 1px solid #2A2A4A; border-radius: 10px; padding: 12px 16px; font-family: monospace; font-size: 14px; color: #6AB86A; display: flex; align-items: center; justify-content: space-between; gap: 12px; margin-top: 12px; cursor: pointer; }
    .cmd-copy { font-size: 11px; color: #555; font-family: sans-serif; flex-shrink: 0; }
    .copied { color: #6AB86A !important; }
    .section-label { max-width: 860px; margin: 0 auto 12px; font-size: 11px; font-weight: 700; letter-spacing: 2px; color: #444; padding-left: 4px; }
    .section-label:not(:first-child) { margin-top: 36px; }
    .footer { text-align: center; margin-top: 48px; font-size: 11px; color: #333; }
  </style>
</head>
<body>
<div class="header">
  <div class="header-badge">MY AI LAB</div>
  <h1>アプリ一覧</h1>
  <p>[あなたの名前]が作ったツール・アプリのランチャー</p>
</div>

<div class="section-label">AI ASSISTANT</div>
<div class="grid" style="margin-bottom:0">
  <div class="card card-claude">
    <div class="claude-inner">
      <span class="claude-icon">🤖</span>
      <div class="claude-info">
        <span class="card-tag tag-tool">TOOL</span>
        <h2>[AI名]（Claude Code）</h2>
        <p>アプリの作成・修正・調査など何でも依頼できるAI。ターミナルから起動します。</p>
        <div class="cmd-box" onclick="copyCmd(this, 'claude')">
          <span>$ claude</span>
          <span class="cmd-copy">クリックでコピー</span>
        </div>
      </div>
    </div>
  </div>
</div>

<div class="section-label" style="margin-top:36px">LOCAL FILES — ローカル</div>
<div class="grid">
  <div class="card">
    <span class="card-icon">📋</span>
    <span class="card-tag tag-local">LOCAL</span>
    <h2>スキル一覧</h2>
    <p>Claude Codeで使えるスキルの一覧。どんなことをAIに頼めるか確認できます。</p>
    <a class="btn-open" href="skill_list.md">開く →</a>
  </div>
  <div class="card">
    <span class="card-icon">🧠</span>
    <span class="card-tag tag-local">LOCAL</span>
    <h2>CLAUDE.md ビューア</h2>
    <p>AIのルール設定を可視化。GREEN/YELLOW/REDの意味やトリガーワードを確認できます。</p>
    <a class="btn-open" href="claude_md_viewer.html">開く →</a>
  </div>
  <div class="card">
    <span class="card-icon">📖</span>
    <span class="card-tag tag-local">LOCAL</span>
    <h2>CLAUDE.md ルール解説</h2>
    <p>各ルールの「なぜ」を解説するリファレンス。設定の背景にある考え方がわかります。</p>
    <a class="btn-open" href="claude_md_rules.html">開く →</a>
  </div>
</div>

<div class="footer">
  最終更新：<span id="date"></span>　|　[あなたの名前] AI Lab
</div>

<script>
  document.getElementById('date').textContent = new Date().toLocaleDateString('ja-JP');
  function copyCmd(el, cmd) {
    navigator.clipboard.writeText(cmd).then(() => {
      const hint = el.querySelector('.cmd-copy');
      hint.textContent = 'コピーしました！';
      hint.classList.add('copied');
      setTimeout(() => { hint.textContent = 'クリックでコピー'; hint.classList.remove('copied'); }, 2000);
    });
  }
</script>
</body>
</html>
```

---

### 14-4: スキル一覧（skill_list.md）

`./skill_list.md` を以下の内容で作成してください。

```markdown
# スキル・コマンド一覧

> このファイルは使えるスキルの一覧です。「/スキル名」で呼び出せます。

---

## コンテンツ・発信

- **`/article-writing`** 記事・長文コンテンツ作成
- **`/content-engine`** SNSコンテンツ量産エンジン（X・LinkedIn・TikTok等）
- **`/crosspost`** SNS一括クロスポスト（X・Threads・Bluesky等）

## 動画・メディア

- **`/fal-ai-media`** AI画像・動画・音声生成（fal.ai経由）
- **`/video-editing`** AI動画編集ワークフロー

## リサーチ・調査

- **`/deep-research`** 深層リサーチ（複数情報源・出典付きレポート）
- **`/market-research`** 市場調査・競合分析

## ビジネス

- **`/investor-materials`** 投資家向け資料作成

## AIエージェント・自動化

- **`/agentic-engineering`** エージェントエンジニアリング設計

## セキュリティ

- **`/security-review`** セキュリティレビュー

## ツール・ユーティリティ

- **`/docx`** Word文書生成
- **`/pptx`** PowerPoint生成

---

## エージェント（委譲・サブタスク用）

- **`architect`** システム設計・技術的意思決定
- **`code-reviewer`** コード品質・セキュリティレビュー
- **`python-reviewer`** Pythonコードレビュー
- **`typescript-reviewer`** TypeScript/JavaScriptレビュー
- **`security-reviewer`** セキュリティ脆弱性検出
- **`database-reviewer`** PostgreSQL・DBのレビュー
- **`deep-research`** 深層リサーチ

---

## スキルの追加方法

**グローバル（全プロジェクトで使いたい）**
→ `~/.claude/skills/` にスキルフォルダをコピー

**このプロジェクト専用**
→ `.claude/skills/スキル名/SKILL.md` を作成
```

---

### 14-5: Claude起動ショートカット（open_claude.command）

> **⚠️ Mac 専用の手順です。**
> Windows の方はターミナル（コマンドプロンプト / PowerShell）から `cd` でこの作業フォルダへ移動 → `claude` と入力して起動してください。このステップはスキップできます。

> ▶ **Mac のみ**: `./open_claude.command` を以下の内容で作成してください。

```bash
#!/bin/bash
cd "$(dirname "$0")"
claude
```

作成後、実行権限を付与してください：

```bash
chmod +x ./open_claude.command
```

---

## Step 15: 動作確認

> ▶ **Mac のみ**: 以下のbashコマンドで確認してください。

```bash
ls ./                         # フォルダが全部あるか（06_AppLaud, 07_タスク 含む）
ls ~/.claude/hooks/           # 3つのPythonスクリプトがあるか
cat ~/.claude/CLAUDE.md       # 名前・SubAgent・A→B→C・vault-maintenanceトリガーが入っているか
cat ./03_私について/my_profile.md
cat ./07_タスク/MASTER_TASKS.md
ls ~/.claude/projects/        # 作業フォルダに対応するプロジェクトフォルダがあるか
cat ./02_設定/.env             # 全4キーの行があるか（値は空でOK）
python3 ./02_設定/vault-maintenance.py index   # エラーなく動作するか
ls ./claude_md_viewer.html ./claude_md_rules.html ./app_launcher.html ./skill_list.md ./open_claude.command
launchctl list | grep com.mycontext   # chatwork-digestジョブが登録されているか
```

---

> ▶ **Windows のみ**: 以下のPowerShellコマンドで確認してください。

```powershell
dir .\                        # フォルダが全部あるか（06_AppLaud, 07_タスク 含む）
dir $HOME\.claude\hooks\      # 3つのPythonスクリプトがあるか
Get-Content $HOME\.claude\CLAUDE.md   # 名前・SubAgent・A→B→C・vault-maintenanceトリガーが入っているか
Get-Content .\03_私について\my_profile.md
Get-Content .\07_タスク\MASTER_TASKS.md
dir $HOME\.claude\projects\   # 作業フォルダに対応するプロジェクトフォルダがあるか
Get-Content .\02_設定\.env     # 全4キーの行があるか（値は空でOK）
python .\02_設定\vault-maintenance.py index    # エラーなく動作するか
dir .\claude_md_viewer.html, .\claude_md_rules.html, .\app_launcher.html, .\skill_list.md
schtasks /query /tn "MyContext\ChatworkDailyDigest"   # タスクが登録されているか
```

> **Windows のみ — 補足**: `open_claude.command` はMac専用のため存在しなくて正常です。

---

全部確認できたら「セットアップ完了です」と報告してください。
