# AIボイスレコーダー化アプリ (AppLaud)

## 概要

AppLaudは、USBボイスレコーダーを接続した際に、音声ファイルを自動的に取り込み、文字起こしと要約を行うアプリケーションです。生成されたテキストはMarkdownファイルとして保存され、日々の音声記録の管理と活用を効率化します。

## 主な機能

*   **自動ファイル取り込み:** 指定されたUSBボイスレコーダーの接続を検知し、音声ファイル（wav, mp3, m4a）を自動でローカルフォルダに移動します。
*   **AIによる文字起こしと要約:** Gemini APIを利用して、音声ファイルの文字起こしと要約を高精度で行います。
*   **Markdown形式での保存:** 要約結果をMarkdownファイルとして、整理された形式で保存します。ファイル名は日付と内容に基づき自動生成されます。
*   **長時間音声対応:** 20分を超える音声ファイルは自動的に分割処理され、APIの制限に対応しつつ、途切れることのない文字起こし結果を得られます。

## システム構成要素

| ファイル | 役割 | Mac | Windows |
|---|---|---|---|
| `script/config.py` | Python設定ファイル（推奨） | ✅ | ✅ |
| `script/file_mover.py` | 音声ファイル移動・処理呼び出し | ✅ | ✅ |
| `script/watch_usb.py` | USB挿抜監視ループ | ✅ | ✅ |
| `script/transcribe_summarize.py` | Gemini API文字起こし・要約 | ✅ | ✅ |
| `script/config.sh` | zsh設定ファイル（Mac従来版） | ✅ | ❌ |
| `script/file_mover.sh` | zshファイル移動スクリプト（Mac従来版） | ✅ | ❌ |
| `script/com.example.applaud.filemover.plist` | launchd設定（Mac従来版） | ✅ | ❌ |

---

## セットアップ（Windows）

### 前提条件

*   Python 3.10 以上
*   [ffmpeg](https://ffmpeg.org/download.html) のインストールとPATHへの追加（mp3/m4a処理に必要）

### 手順

**1. リポジトリのクローン**

MyContextの作業フォルダ内にクローンしてください（パス設定が自動解決されます）。

```powershell
# 例: J:\GoogleApp\Claudecode\ で起動している場合
git clone https://github.com/tonsuke1003-wq/AppLaud.git
```

**2. 依存ライブラリのインストール**

```powershell
pip install -r requirements.txt
```

**3. APIキーの設定**

`../02_設定/.env`（MyContextの作業フォルダ内）を開き、Gemini APIキーを設定してください。

```
GEMINI_API_KEY=your_api_key_here
```

> APIキーは [Google AI Studio](https://aistudio.google.com/) で取得できます。

**4. 設定ファイルの編集**

`script/config.py` を開き、必要に応じて設定してください。

```python
# ボイスレコーダーのドライブ文字（例: "E:\\"）
# 空文字列にすると全リムーバブルドライブを対象にする
RECORDER_DRIVE = ""

# レコーダー内の音声ファイルサブディレクトリ（例: "RECORD"）
VOICE_FILES_SUBDIR = "RECORD"
```

**5. USB監視の起動**

```powershell
python script/watch_usb.py
```

ボイスレコーダーをUSB接続すると自動で処理が開始されます。`Ctrl+C` で停止。

**手動実行（USB接続済みのドライブを即時処理）：**

```powershell
python script/watch_usb.py --once
# または
python script/file_mover.py E:\
```

**6. Windowsタスクスケジューラーで起動時に自動実行する（任意）**

PowerShellを管理者権限で実行：

```powershell
$scriptPath = "[AppLaudのパス]\script\watch_usb.py"
$pythonPath = (Get-Command python).Source

schtasks /create `
  /tn "AppLaud\WatchUSB" `
  /tr "`"$pythonPath`" `"$scriptPath`"" `
  /sc ONLOGON `
  /ru "$env:USERNAME" `
  /f

Write-Host "✅ 登録完了"
```

---

## セットアップ（Mac）

**1. リポジトリのクローン**

```bash
git clone https://github.com/tonsuke1003-wq/AppLaud.git ~/Desktop/AppLaud
cd ~/Desktop/AppLaud
```

**2. 設定ファイルの編集**

`script/config.sh` を開き、環境に合わせて設定してください。

```bash
export RECORDER_NAME="RECORDER"        # USBボリューム名
export VOICE_FILES_SUBDIR="RECORD"     # サブディレクトリ名
export AUDIO_DEST_DIR="/path/to/audio" # 音声ファイル移動先
export MARKDOWN_OUTPUT_DIR="/path/to/markdown_output" # 要約出力先
```

**3. 依存ライブラリのインストール**

```bash
pip install -r requirements.txt
```

**4. APIキーの設定**

```bash
export GOOGLE_API_KEY="YOUR_API_KEY"
```

**5. USB監視の起動（2つの方法）**

**方法A: Python スクリプト（Windows と同じ手順・推奨）**

```bash
python3 script/watch_usb.py
```

**方法B: launchd エージェント（Mac従来方式）**

```bash
cp script/com.example.applaud.filemover.plist ~/Library/LaunchAgents/
# ~/Library/LaunchAgents/com.example.applaud.filemover.plist を編集してパスを設定
launchctl load ~/Library/LaunchAgents/com.example.applaud.filemover.plist
```

---

## 使い方

1.  上記セットアップを完了します。
2.  ボイスレコーダーをUSB接続します。
3.  自動的に処理が開始され、`MARKDOWN_OUTPUT_DIR`（デフォルト: `[作業フォルダ]/06_AppLaud/`）に要約Markdownファイルが生成されます。
4.  処理済みの音声ファイルは `AUDIO_DEST_DIR`（デフォルト: `[作業フォルダ]/06_AppLaud/audio/`）に移動されます。
5.  処理のログは `[作業フォルダ]/06_AppLaud/processed_log.jsonl` に記録されます。

---

## 注意事項

*   mp3/m4a ファイルの処理には ffmpeg のインストールが必要です（wav のみ使用する場合は不要）。
*   APIキーの取り扱いには十分注意してください。`.env` ファイルはバージョン管理に含めないでください。
*   長時間音声の処理には時間がかかる場合があります。

## 今後の改善点 (TODO)

*   より詳細なエラーハンドリングと通知機能。
*   Web UIによる設定や操作インターフェース。
*   `launchd.plist` の設定を簡略化する補助スクリプト。

詳細は `document/project.md` を参照してください。
