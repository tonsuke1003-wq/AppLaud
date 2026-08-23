私専用のコンテキストシステム「MyContext」を構築してください。
以下のステップを順番に、すべて完了するまで止まらず実行してください。

---

## Step 0: 前提チェックとOS確認【共通】

**ここで足りないものがあると、後半のステップで必ず失敗します。**
先に全部そろえてから Step 1 へ進んでください。

### 0-1: OSを判定する

あなた（Claude Code）は、起動時に実行環境のOSを把握しています。**まずそれを1行で宣言してください。**
そのうえで、裏を取るために次のどちらかを実行します：

- Macだと思う場合: `uname -s` → `Darwin` と出れば **Mac**
- Windowsだと思う場合: `cmd /c ver` → `Microsoft Windows [Version ...]` と出れば **Windows**

> **OS判定に `python3` を使わないでください。**
> Windows では `python3` が Microsoft Store のスタブに割り当てられていることがあり、
> 何も出力せずに終了したり、ストアのページが開いたりして判定に失敗します。

以降、`▶ Mac のみ` と書かれたセクションはMacのみ実行、`▶ Windows のみ` はWindowsのみ実行してください。
それ以外のセクションは **両OS共通** です。

### 0-2: 前提ツールをチェックする

> ▶ **Mac のみ**:
> ```bash
> echo "--- 前提チェック ---"
> command -v git     >/dev/null && echo "✅ git     $(git --version)"     || echo "❌ git 未導入 → xcode-select --install"
> command -v python3 >/dev/null && echo "✅ python3 $(python3 --version)" || echo "❌ python3 未導入 → https://www.python.org/downloads/"
> command -v claude  >/dev/null && echo "✅ claude  $(claude --version)"  || echo "❌ claude CLI が PATH にない"
> command -v ffmpeg  >/dev/null && echo "✅ ffmpeg  導入済み"             || echo "⚠️ ffmpeg 未導入 → brew install ffmpeg（Step 8で必要）"
> python3 -c "import sys; v=sys.version_info; print('✅ Python %d.%d はOK' % v[:2]) if v >= (3,10) else print('❌ Python 3.10以上が必要（現在 %d.%d）' % v[:2])"
> ```

> ▶ **Windows のみ**:
> ```powershell
> Write-Host "--- 前提チェック ---"
> foreach ($t in @("git","python","claude","ffmpeg")) {
>     $c = Get-Command $t -ErrorAction SilentlyContinue
>     if ($c) { Write-Host "OK   $t : $($c.Source)" } else { Write-Host "NG   $t が見つかりません" }
> }
> python -c "import sys; v=sys.version_info; print('OK   Python %d.%d' % v[:2]) if v >= (3,10) else print('NG   Python 3.10以上が必要')"
> ```

**❌ / NG が1つでも出たら、そのツールを先に導入してください。**

| ツール | 用途 | 無いとどうなるか |
|---|---|---|
| git | Step 8 で AppLaud をクローンする | Step 8 で停止 |
| python | ほぼ全ステップ | Step 5 以降が全滅 |
| claude CLI | 完成後の起動 | セットアップは通るが使えない |
| ffmpeg | mp3/m4a の音声処理 | **セットアップは成功し、録音を挿した日に初めて失敗する** |

> ▶ **Windows のみ**: `python` が反応せず Microsoft Store が開く場合は、
> Pythonランチャー `py` を試してください（`py --version`）。
> それでもダメなら [python.org](https://www.python.org/downloads/) からインストールし、
> インストーラの **「Add python.exe to PATH」に必ずチェック**を入れてください。

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

## Step 2: .env と .gitignore を作成する【共通】

### 2-1: .env

`./02_設定/.env` を作成してください。
内容は以下のみ（`GEMINI_MODEL` 以外の値は私があとでエディタで直接入力します）：

```
GEMINI_API_KEY=
GEMINI_MODEL=gemini-flash-latest
CW_TOKEN=
CW_NOTIFY_TOKEN=
CW_TARGET_ROOM=
```

> **`GEMINI_MODEL` は「常に最新のFlash」を指すエイリアスです。**
> 全スクリプトがこの1行だけを参照するので、モデルを差し替えたくなったらここを書き換えるだけで済みます。
> プレビュー版のモデルID（`*-preview`）を各スクリプトに直書きすると、提供終了と同時に全部まとめて止まります。

### 2-2: .gitignore【必須・スキップ禁止】

`.env` には APIキーが入ります。作業フォルダをGitで管理した瞬間に流出するので、
**`.env` を作ったらすぐ** `./.gitignore` を作成してください：

```
# APIキー（絶対にコミットしない）
02_設定/.env

# 会話ログ・音声・日記（プライベート情報）
05_日記/
06_AppLaud/

# Python
.venv/
__pycache__/
*.pyc
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

## Step 4: CLAUDE.md を2枚作成する【共通】

CLAUDE.md は**2層に分けます**：

| ファイル | 読まれるタイミング | 何を書くか |
|---|---|---|
| `~/.claude/CLAUDE.md`（グローバル） | **どのフォルダで claude を起動しても必ず** | 人格・GREEN/YELLOW/RED・A→B→C・memoryルールなど**場所に依存しない**ルール |
| `[作業フォルダ]/CLAUDE.md`（プロジェクト） | この作業フォルダで起動したときだけ | トリガーワード表・フォルダ構成・`./02_設定/` などの**相対パスを含む**ルール |

> **なぜ分けるのか**: グローバルCLAUDE.mdは全プロジェクトで読まれます。
> ここに `./07_タスク/MASTER_TASKS.md` のような相対パスを書いてしまうと、
> 別のフォルダで claude を起動したときに、存在しないパスを指示し続けることになります。

### 4-1: ~/.claude/CLAUDE.md（グローバル）

【重要】既存のファイルがある場合は上書きせず、末尾に追記してください。
**すでに `## [AI名] — ` の見出しが存在する場合は、2回目の実行なので追記せず、差分だけ反映してください**（追記すると内容が二重化します）。

以下の内容をそのまま書き込んでください。
[あなたの名前] の部分はStep3で聞いた名前に置き換えてください。
[AI名] の部分はあなたの好きな名前を入れてください（例: レイ、ハル、Aiなど）。

```markdown
## [AI名] — [あなたの名前]専用AIビジネスパートナー

- このClaudeは**[AI名]**として動作する（オーナー: [あなたの名前]）
- ミッション: **Claudeが作業を担い、[あなたの名前]は承認のみ**。手間最小化・自動化を最優先
- MyContextの作業フォルダで起動したときは、そのフォルダの `./CLAUDE.md` に
  プロフィール・トリガーワード・各スクリプトのパスが書いてある

---

## 行動原則

- **削除禁止** → ゴミ箱フォルダへ移動する（移動先は各プロジェクトの CLAUDE.md 参照）
- 不可逆操作（外部公開・決済・外部API送信）は確認なしに実行しない
- secrets/APIキー → コードに書かない・環境変数使用（.envを参照）
- `.env` を扱う前に、必ず `.gitignore` に入っているか確認する

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

## サブエージェント ルーティング

「レビューして」「サブエージェントでチェックして」と言われたら、直前の作業に合わせて最適なエージェントを起動する。

**この表には実在するエージェント名しか書かないこと。** 存在しない名前を指定すると、
Claudeは黙って汎用エージェントにフォールバックする。レビュー結果は返ってくるので、
「指定した専門エージェントが動いていない」ことに誰も気づけない。

| 直前の作業 | 起動するエージェント | 出どころ |
|---|---|---|
| コード全般のレビュー | `code-reviewer` | pr-review-toolkit |
| エラーの握りつぶし・失敗の見落とし | `silent-failure-hunter` | pr-review-toolkit |
| テストの過不足 | `pr-test-analyzer` | pr-review-toolkit |
| 型設計・データ構造 | `type-design-analyzer` | pr-review-toolkit |
| コメントの質 | `comment-analyzer` | pr-review-toolkit |
| 冗長なコードの整理 | `code-simplifier` | pr-review-toolkit |
| 設計・方針の検討 | `Plan` | Claude Code 組み込み |
| コードの場所を横断的に探す | `Explore` | Claude Code 組み込み |
| セキュリティ | `/security-review`（スキル） | Claude Code 組み込み |

> **Python専用・TypeScript専用・DB専用のレビューエージェントは存在しない。**
> 言語を問わず `code-reviewer` が担当する。
> PR全体をまとめてレビューしたい時は `/review-pr` を使う。

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
```

---

### 4-2: [作業フォルダ]/CLAUDE.md（プロジェクト）

作業フォルダ直下に `./CLAUDE.md` を作成してください。
**相対パスを含むルールはすべてこちらに置きます**（このフォルダで起動したときだけ読まれるため）。
[AI名] は 4-1 で決めた名前に置き換えてください。

```markdown
# MyContext — このフォルダのルール

> このファイルは、この作業フォルダで Claude Code を起動したときだけ読み込まれる。
> AIの人格・GREEN/YELLOW/RED・A→B→C などの共通ルールは `~/.claude/CLAUDE.md` 側にある。

## このフォルダのパス

- プロフィール: `./03_私について/my_profile.md`
- 設定・APIキー: `./02_設定/.env`（**`.gitignore` 済み。中身をチャットに出力しない**）
- 削除禁止 → 消さずに `./00_ゴミ箱/` へ移動する
- Geminiのモデル名は `./02_設定/.env` の `GEMINI_MODEL` を唯一の情報源とする
  （スクリプトにモデルIDを直書きしない）
- AppLaud関連スクリプトは **`.venv` のPython** で実行する
  （Mac: `./.venv/bin/python` / Windows: `.\.venv\Scripts\python.exe`）

## フォルダ構成

| フォルダ | 用途 |
|---|---|
| `00_ゴミ箱/` | 削除の代わりに移動する先 |
| `01_事業・クライアント/` | 案件ごとの資料 |
| `02_設定/` | .env・pipeline.py・vault-maintenance.py・chatwork-daily-digest.py |
| `03_私について/` | my_profile.md（AIが参照する自己紹介） |
| `04_ナレッジ/` | `切り抜き/`（未整理素材） → `情報源/`（Wiki化済み） |
| `05_日記/` | 日報・`チャットログ/` |
| `06_AppLaud/` | 音声メモの文字起こし・要約の出力先 |
| `07_タスク/` | MASTER_TASKS.md |

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
        # 現行の PreToolUse スキーマ: stdout に hookSpecificOutput を出して exit 0。
        # 旧 {"decision": "block"} + exit 2 は非推奨で、しかも exit 2 では stdout が
        # 表示されないため「なぜ止まったか」が本人に伝わらない。
        print(json.dumps({
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": "⛔ APIキーが出力に含まれています。.envファイルを直接参照してください。"
            }
        }, ensure_ascii=False))
        sys.exit(0)
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
    # MultiEdit / NotebookEdit も検査対象に含める（漏れると素通りする）
    if tool_name not in ("Write", "Edit", "MultiEdit", "NotebookEdit"):
        sys.exit(0)
    file_path = tool_input.get("file_path", "")
    if is_safe_file(file_path) or file_path.endswith(".env"):
        sys.exit(0)
    if tool_name == "Write":
        content = tool_input.get("content", "")
    elif tool_name == "MultiEdit":
        content = "\n".join(e.get("new_string", "") for e in tool_input.get("edits", []))
    elif tool_name == "NotebookEdit":
        content = tool_input.get("new_source", "")
    else:
        content = tool_input.get("new_string", "")
    findings = []
    for pattern, name in SECRET_PATTERNS:
        if re.search(pattern, content):
            findings.append(name)
    if findings:
        print(json.dumps({
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": f"シークレット漏洩の可能性: {', '.join(findings)}\nAPIキーは.envファイルに保存してください。"
            }
        }, ensure_ascii=False))
        sys.exit(0)
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

    # このhookは全プロジェクトで発火する。cwd直下に無条件で 05_日記/ を作ると、
    # 無関係なリポジトリに会話ログが生成され、そのままコミットされる事故になる。
    # → 05_日記/ が既に在るフォルダ（＝MyContext作業フォルダ）でだけ保存する。
    cwd = data.get("cwd", "")
    journal_dir = Path(cwd) / "05_日記" if cwd else None
    if journal_dir is not None and journal_dir.is_dir():
        save_dir = journal_dir / "チャットログ"
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

【重要】既存のsettings.jsonがある場合は**上書き禁止**。次のルールでマージしてください：

- `"permissions"` … **既存の設定があるなら一切触らない**（キー自体が無い場合だけ追加する）
- `"hooks"` … 既存の同名イベントがあれば配列に追加。**同じ command が既にあれば重複登録しない**（2回目の実行対策）

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
        "matcher": "Write|Edit|MultiEdit|NotebookEdit",
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

> **⚠️ JSONが壊れると hooks は無言で全滅します（エラーも出ません）。** 書き込んだら必ず検証してください：
>
> - Mac: `python3 -m json.tool ~/.claude/settings.json > /dev/null && echo "✅ JSON OK"`
> - Windows: `python -m json.tool $HOME\.claude\settings.json > $null; if ($?) { "✅ JSON OK" }`

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

    # user-prompt-save.py と同じ理由で、05_日記/ が既に在るフォルダでだけ保存する。
    # （会話全文を無関係なリポジトリに書き出さないため）
    journal_dir = Path(project_cwd) / "05_日記" if project_cwd else None
    if journal_dir is not None and journal_dir.is_dir():
        save_dir = journal_dir / "チャットログ"
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

### 8-1: クローン

作業フォルダ内に AppLaud をクローンします（Mac/Windows両対応のフォーク版）：

> ▶ **Mac のみ**: `git clone https://github.com/tonsuke1003-wq/AppLaud.git ./AppLaud`

> ▶ **Windows のみ**: `git clone https://github.com/tonsuke1003-wq/AppLaud.git ./AppLaud`

### 8-2: 仮想環境（.venv）を作って依存パッケージを入れる

【重要】`pip3 install` をシステムのPythonへ直接実行すると、最近のMacでは
`error: externally-managed-environment` で**必ず失敗します**（PEP 668）。
**作業フォルダ直下に `.venv` を作り、AppLaud関連はすべてそのPythonで動かします。**

> ▶ **Mac のみ**:
> ```bash
> python3 -m venv .venv
> ./.venv/bin/python -m pip install --upgrade pip
> ./.venv/bin/python -m pip install -r ./AppLaud/requirements.txt
> ./.venv/bin/python -c "import google.genai, pydub, psutil; print('✅ 依存パッケージOK')"
> ```

> ▶ **Windows のみ**:
> ```powershell
> python -m venv .venv
> .\.venv\Scripts\python.exe -m pip install --upgrade pip
> .\.venv\Scripts\python.exe -m pip install -r .\AppLaud\requirements.txt
> .\.venv\Scripts\python.exe -c "import google.genai, pydub, psutil; print('OK')"
> ```

> **以降、AppLaud を動かすときは必ず `.venv` のPythonを使ってください。**
> `python3` / `python` と打つとパッケージの入っていない別のPythonが動き、`ModuleNotFoundError` になります。
>
> | | .venv の Python |
> |---|---|
> | Mac | `./.venv/bin/python` |
> | Windows | `.\.venv\Scripts\python.exe` |
>
> ※ `~/.claude/hooks/` の3本と `02_設定/` の3本は**標準ライブラリだけ**で動くので、
> 　`python3` / `python` のままで構いません（グローバル設定を特定プロジェクトのvenvに依存させないための設計です）。

### 8-3: ffmpeg（必須）

mp3/m4a の処理に ffmpeg が必要です。**未導入でも今日は何も起きず、録音を挿した日に初めて失敗します。**
必ずこの場で確認してください。

> ▶ **Mac のみ**:
> ```bash
> ffmpeg -version >/dev/null 2>&1 && echo "✅ ffmpeg OK" || echo "❌ 未インストール → brew install ffmpeg"
> ```

> ▶ **Windows のみ**:
> ```powershell
> if (Get-Command ffmpeg -ErrorAction SilentlyContinue) { "✅ ffmpeg OK" } else { "❌ 未インストール → https://ffmpeg.org/download.html からインストールしPATHへ追加" }
> ```

### 8-4: config.py の確認

`./AppLaud/script/config.py` を開いて設定を確認してください：

```python
# ボイスレコーダーのドライブ/ボリューム（空文字列で全リムーバブルドライブを対象）
# Mac例: "/Volumes/IC RECORDER"  Windows例: "E:\\"
RECORDER_DRIVE = ""

# レコーダー内の音声ファイルサブディレクトリ（例: "RECORD" または ""）
VOICE_FILES_SUBDIR = "RECORD"
```

> APIキー（`GEMINI_API_KEY`）は `./02_設定/.env` から自動読み込みされます。`config.py` に直接書かないでください。

### 8-5: 起動

USB監視を起動するには（**必ず .venv のPython**）：

> ▶ **Mac のみ**: `./.venv/bin/python ./AppLaud/script/watch_usb.py`

> ▶ **Windows のみ**: `.\.venv\Scripts\python.exe .\AppLaud\script\watch_usb.py`

ボイスレコーダーを接続すると自動で処理が開始されます（Ctrl+C で停止）。

手動実行（接続済みドライブを即時処理）：

> ▶ **Mac のみ**: `./.venv/bin/python ./AppLaud/script/watch_usb.py --once`

> ▶ **Windows のみ**: `.\.venv\Scripts\python.exe .\AppLaud\script\watch_usb.py --once`

**（上級）ログイン時に自動起動する場合：**

> ▶ **Mac のみ**: launchd で設定します。

```bash
WORK_DIR=$(pwd)
PYTHON_PATH="${WORK_DIR}/.venv/bin/python"   # ← システムのpython3ではなく .venv を指す
if [ ! -x "$PYTHON_PATH" ]; then echo "❌ .venv が見つかりません。Step 8-2 を先に実行してください"; exit 1; fi

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

# .venv のPythonを使う。pythonw.exe = 起動のたびに黒いコンソール窓が出ない
$pythonPath = "$workDir\.venv\Scripts\pythonw.exe"
if (-not (Test-Path $pythonPath)) {
    Write-Error ".venv が見つかりません。Step 8-2 を先に実行してください"
    exit 1
}

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
FALLBACK_GEMINI_MODEL = "gemini-flash-latest"   # .env に GEMINI_MODEL が無い場合だけ使う

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

def get_gemini_model() -> str:
    env = load_env(ENV_PATH)
    return env.get("GEMINI_MODEL", "") or os.environ.get("GEMINI_MODEL", "") or FALLBACK_GEMINI_MODEL

def extract_gemini_text(data: dict) -> str:
    """Geminiのレスポンスから本文テキストを取り出す。

    Gemini 3系は thinking がデフォルトで有効。parts[0] が思考パート（textキーなし）だったり、
    出力上限に当たって text が1つも返らないことがあるため、
    parts[0]["text"] の直参照は KeyError で落ちる。必ず全partsを走査する。
    """
    for cand in data.get("candidates", []):
        parts = cand.get("content", {}).get("parts", []) or []
        texts = [p["text"] for p in parts
                 if isinstance(p, dict) and p.get("text") and not p.get("thought")]
        if texts:
            return "\n".join(texts).strip()
        if cand.get("finishReason") == "MAX_TOKENS":
            print("  ⚠️ 出力上限に到達（maxOutputTokensを増やしてください）", file=sys.stderr)
    return ""

def gemini_generate(prompt: str, api_key: str, model: str = "") -> str:
    model = model or get_gemini_model()
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    payload = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"maxOutputTokens": 8192, "temperature": 0.3},
    }, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=60) as res:
            return extract_gemini_text(json.load(res))
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

## Step 12: AppLaud タスク抽出スクリプトを確認する【共通】

**このステップではファイルを作成しません。**
`extract_tasks.py` は Step 8 でクローンしたリポジトリに**最新版が同梱されています**
（`./AppLaud/script/extract_tasks.py`）。

> ⚠️ **絶対に上書きしないでください。**
> リポジトリ側の `extract_tasks.py` は Gemini の新SDK・最新モデル名に更新済みです。
> ここで古いコードを書き込むと修正が巻き戻り、さらに次回以降 `git pull` するたびに
> コンフリクトして更新を受け取れなくなります。

存在確認と動作確認だけしてください：

> ▶ **Mac のみ**:
> ```bash
> ls -l ./AppLaud/script/extract_tasks.py
> git -C ./AppLaud status --short        # 出力が空 = 上書きしていない（正常）
> python3 ./AppLaud/script/extract_tasks.py
> ```

> ▶ **Windows のみ**:
> ```powershell
> dir .\AppLaud\script\extract_tasks.py
> git -C .\AppLaud status --short        # 出力が空 = 上書きしていない（正常）
> python .\AppLaud\script\extract_tasks.py
> ```

`06_AppLaud/` にはまだ音声メモが無いので、
**「直近24時間のAppLaudファイルが見つかりません」と表示されれば正常です**（エラーではありません）。

> このスクリプトは `./06_AppLaud/` の要約を読み、`./07_タスク/MASTER_TASKS.md` に追記します。
> CLAUDE.md の「AppLaudからタスク抽出」トリガーから呼ばれます。
>
> **重複防止つきです。** 「AppLaudからタスク抽出」を何度言っても同じタスクは増えません：
> ① 処理済みの音声メモは `./07_タスク/.extract_tasks_state.json` に記録してスキップ
> ② MASTER_TASKS.md に同じ文面が既にあるタスクは追加しない
> 記録を無視して抽出し直したい場合だけ `--force` を付けて実行します。
> 使用モデルは `./02_設定/.env` の `GEMINI_MODEL` を参照します（スクリプトへの直書きはしません）。
> 標準ライブラリだけで動くので、`.venv` ではなく `python3` / `python` で実行して構いません。

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
GEMINI_MODEL    = _ENV.get("GEMINI_MODEL", "")    or os.environ.get("GEMINI_MODEL", "") or "gemini-flash-latest"
GEMINI_URL      = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent"

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

def extract_gemini_text(data):
    """Gemini 3系は thinking が有効で parts[0] に text が無い場合がある。
    parts[0]["text"] 直参照は KeyError で落ちるため、全partsを走査する。"""
    for cand in data.get("candidates", []):
        parts = cand.get("content", {}).get("parts", []) or []
        texts = [p["text"] for p in parts
                 if isinstance(p, dict) and p.get("text") and not p.get("thought")]
        if texts:
            return "\n".join(texts).strip()
        if cand.get("finishReason") == "MAX_TOKENS":
            log("⚠️ 出力上限に到達（maxOutputTokensを増やしてください）")
    return ""

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
        "generationConfig": {"maxOutputTokens": 8192, "temperature": 0.7},
    }, ensure_ascii=False).encode("utf-8")

    url = f"{GEMINI_URL}?key={GEMINI_API_KEY}"
    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=60) as res:
            return extract_gemini_text(json.load(res)) or None
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
</dict>
</plist>
EOF

launchctl load ~/Library/LaunchAgents/com.mycontext.chatwork-digest.plist
echo "✅ launchd に登録しました（毎朝5:00のみ実行）"
```

> **`RunAtLoad` は意図的に外しています。**
> 有効にすると、この登録コマンドを打った瞬間と、以後ログインするたびに
> Chatworkへブリーフィングが送信されます（＝無確認の外部送信）。
> CLAUDE.md で「外部送信 = RED（必ず承認）」と定めている以上、
> セットアップが勝手に送信を発火させてはいけません。送信は下の手動テストで1回だけ行います。

> **⚠️ launchd の 5:00 はMacの電源状態に左右されます。**
> スリープ中なら次に起きたタイミングでまとめて実行され、電源が落ちていればその日はスキップされます。
> 毎朝確実に受け取りたい場合は、システム設定 > バッテリー（省エネルギー）でスケジュール起動を併用してください。

手動テスト（**Chatworkに実際に1通送信されます**）：
```bash
python3 ./02_設定/chatwork-daily-digest.py
```

---

> ▶ **Windows のみ**: Windowsタスクスケジューラーで設定します。

PowerShellを**管理者権限**で実行してください：

```powershell
$workDir    = (Get-Location).Path
$scriptPath = "$workDir\02_設定\chatwork-daily-digest.py"

# 注: `?.`（null条件演算子）は PowerShell 7以降専用。
# Windows標準の PowerShell 5.1 では構文エラーになり、スクリプト全体が実行されない。
$cmd = Get-Command python -ErrorAction SilentlyContinue
if (-not $cmd) { $cmd = Get-Command py -ErrorAction SilentlyContinue }
if (-not $cmd) { Write-Error "Pythonが見つかりません。PythonをインストールしPATHへ追加してください"; exit 1 }
$pythonPath = $cmd.Source

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

## Step 14: 公式プラグインの導入とダッシュボード作成

公式マーケットプレイスからプラグインを導入し、そのあとダッシュボード5ファイルを作成します。

### 14-0: 公式プラグインを導入する【共通】

Step 4-1 のサブエージェント表が指すエージェント（`code-reviewer` など）と、
Word/PowerPoint生成スキル（`/docx` `/pptx`）は、**プラグインを入れて初めて実在します。**
入れないまま表だけ書くと、Claudeは黙って汎用エージェントにフォールバックし、
「動いていないのに動いているように見える」状態になります。

以下を順に実行してください（Mac/Windows共通・対話プロンプトなし）：

```bash
# マーケットプレイスを登録
claude plugin marketplace add anthropics/skills

# プラグインを導入（--scope user = 全プロジェクトで有効）
claude plugin install document-skills@anthropic-agent-skills   -y --scope user
claude plugin install pr-review-toolkit@claude-plugins-official -y --scope user
claude plugin install claude-md-management@claude-plugins-official -y --scope user
claude plugin install skill-creator@claude-plugins-official    -y --scope user

# 確認
claude plugin list
```

> `claude-plugins-official` は最初から登録済みなので、追加が必要なのは `anthropics/skills` だけです。

導入されるものと、毎セッションのコンテキスト消費：

| プラグイン | 中身 | 常時コスト |
|---|---|---|
| `document-skills` | `/docx` `/pptx` `/xlsx` `/pdf` の4スキル | 約1,030トークン |
| `pr-review-toolkit` | `code-reviewer` ほか**6エージェント** + `/review-pr` | 約2,030トークン |
| `claude-md-management` | CLAUDE.mdの改善・棚卸しスキル2種 | 約175トークン |
| `skill-creator` | 自分専用スキルを作るスキル | 約112トークン |
| **合計** | | **約3,350トークン** |

> **反映には Claude Code の再起動が必要です。** 導入後、一度終了して起動し直してください。

> **入れてはいけない組み合わせ**: `feature-dev` も `code-reviewer` という同名エージェントを持つため、
> `pr-review-toolkit` と同時に入れると名前が衝突します。どちらか一方にしてください。
> 同様に `code-simplifier` 単体プラグインは `pr-review-toolkit` に同梱済みなので不要です。

> **任意**: `security-guidance` を入れると、編集時の警告・Stop時のLLM差分レビュー・
> コミット前の脆弱性チェックが追加されます。**コンテキスト消費はゼロ**（hooksのみ）ですが、
> セッション終了のたびに追加のLLM呼び出しが走るため、コストとレイテンシが増えます。
> Step 5 で入れた自作hooksで足りていると感じるなら、無理に入れる必要はありません。
> 入れる場合: `claude plugin install security-guidance@claude-plugins-official -y --scope user`

---

### 14-1〜14-5: ダッシュボード

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

> **ここに載っているのは、実際にこのPCで動くものだけです。**
> 手元にあるものと一覧がズレると「叩いても動かない」状態になるので、
> 増やしたら必ずこのファイルも更新してください。
> 現在の導入状況は `claude plugin list` で確認できます。

---

## 書類を作る（document-skills）

- **`/docx`** Word文書の生成・編集
- **`/pptx`** PowerPointスライドの生成・編集
- **`/xlsx`** Excelブックの生成・編集
- **`/pdf`** PDFの読み取り・生成

## コードを見てもらう

- **`/review-pr`** 変更内容をまとめてレビュー（pr-review-toolkit）
- **`/security-review`** セキュリティレビュー（Claude Code 組み込み）
- **`/code-review`** 差分のコードレビュー（Claude Code 組み込み）

## AIの設定を育てる

- **`/skill-creator`** 自分専用のスキルを作る・改善する
- **`claude-md-improver`** CLAUDE.md の品質を監査して改善案を出す
- **`revise-claude-md`** セッションでの学びを CLAUDE.md に取り込む

---

## エージェント（委譲・サブタスク用）

「レビューして」と言うと、CLAUDE.md のルーティング表に従って自動で選ばれます。

| エージェント | 役割 | 出どころ |
|---|---|---|
| `code-reviewer` | コード全般のレビュー（**言語を問わない**） | pr-review-toolkit |
| `silent-failure-hunter` | エラーの握りつぶし・失敗の見落としを探す | pr-review-toolkit |
| `pr-test-analyzer` | テストの過不足を見る | pr-review-toolkit |
| `type-design-analyzer` | 型設計・データ構造を見る | pr-review-toolkit |
| `comment-analyzer` | コメントの質を見る | pr-review-toolkit |
| `code-simplifier` | 冗長なコードを整理する | pr-review-toolkit |
| `Plan` | 設計・実装方針を立てる | Claude Code 組み込み |
| `Explore` | コードの場所を横断的に探す | Claude Code 組み込み |

> **`python-reviewer` `typescript-reviewer` `database-reviewer` `architect` は存在しません。**
> 言語別のレビューエージェントは無く、`code-reviewer` が全言語を担当します。
> 設計の相談は `Plan` を使ってください。

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
cat ./.gitignore              # 【最重要】02_設定/.env の行があるか
ls ~/.claude/hooks/           # 3つのPythonスクリプトがあるか
python3 -m json.tool ~/.claude/settings.json > /dev/null && echo "✅ settings.json のJSONは壊れていない"
cat ~/.claude/CLAUDE.md       # 人格・GREEN/YELLOW/RED・A→B→C・memory（相対パスが無いこと）
cat ./CLAUDE.md               # トリガーワード表・フォルダ構成（プロジェクト側）
cat ./03_私について/my_profile.md
cat ./07_タスク/MASTER_TASKS.md
ls ~/.claude/projects/        # 作業フォルダに対応するプロジェクトフォルダがあるか
cat ./02_設定/.env             # 全5キーの行があるか（GEMINI_MODEL 以外は値が空でOK）
./.venv/bin/python -c "import google.genai, pydub, psutil; print('✅ .venv 依存パッケージOK')"
ls -l ./AppLaud/script/extract_tasks.py   # リポジトリ同梱版が存在するか
git -C ./AppLaud status --short           # 出力が空 = 上書きしていない（正常）
python3 ./02_設定/vault-maintenance.py index   # エラーなく動作するか
claude plugin list                    # 4プラグインが enabled になっているか
ls ./claude_md_viewer.html ./claude_md_rules.html ./app_launcher.html ./skill_list.md ./open_claude.command
launchctl list | grep com.mycontext   # chatwork-digestジョブが登録されているか
```

---

> ▶ **Windows のみ**: 以下のPowerShellコマンドで確認してください。

```powershell
dir .\                        # フォルダが全部あるか（06_AppLaud, 07_タスク 含む）
Get-Content .\.gitignore      # 【最重要】02_設定/.env の行があるか
dir $HOME\.claude\hooks\      # 3つのPythonスクリプトがあるか
python -m json.tool $HOME\.claude\settings.json > $null; if ($?) { "✅ settings.json のJSONは壊れていない" }
Get-Content $HOME\.claude\CLAUDE.md   # 人格・GREEN/YELLOW/RED・A→B→C・memory（相対パスが無いこと）
Get-Content .\CLAUDE.md       # トリガーワード表・フォルダ構成（プロジェクト側）
Get-Content .\03_私について\my_profile.md
Get-Content .\07_タスク\MASTER_TASKS.md
dir $HOME\.claude\projects\   # 作業フォルダに対応するプロジェクトフォルダがあるか
Get-Content .\02_設定\.env     # 全5キーの行があるか（GEMINI_MODEL 以外は値が空でOK）
.\.venv\Scripts\python.exe -c "import google.genai, pydub, psutil; print('.venv OK')"
dir .\AppLaud\script\extract_tasks.py   # リポジトリ同梱版が存在するか
git -C .\AppLaud status --short           # 出力が空 = 上書きしていない（正常）
python .\02_設定\vault-maintenance.py index    # エラーなく動作するか
claude plugin list                    # 4プラグインが enabled になっているか
dir .\claude_md_viewer.html, .\claude_md_rules.html, .\app_launcher.html, .\skill_list.md
schtasks /query /tn "MyContext\ChatworkDailyDigest"   # タスクが登録されているか
```

> **Windows のみ — 補足**: `open_claude.command` はMac専用のため存在しなくて正常です。

---

全部確認できたら「セットアップ完了です」と報告してください。
