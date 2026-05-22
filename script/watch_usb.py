#!/usr/bin/env python3
"""
watch_usb.py — AppLaud Windows USB監視スクリプト
launchd + .plist の代替。

ボイスレコーダーのUSB接続を検知して、自動的にfile_mover.pyを実行します。
3秒ごとにドライブの挿抜をポーリングで監視します。

使用法:
  python watch_usb.py            # 監視開始（Ctrl+Cで停止）
  python watch_usb.py --once     # 一度だけドライブを確認して処理（手動実行用）

Windowsタスクスケジューラーで起動時に自動実行する場合:
  タスクスケジューラー → 新しいタスク → トリガー: ログオン時
  操作: python watch_usb.py
"""

import sys
import time
import subprocess
from pathlib import Path

try:
    import psutil
except ImportError:
    print("エラー: psutil がインストールされていません。")
    print("インストール: pip install psutil")
    sys.exit(1)

# config.py から設定を読み込む
sys.path.insert(0, str(Path(__file__).parent))
from config import RECORDER_DRIVE, TARGET_EXTENSIONS

POLL_INTERVAL_SEC = 3  # ドライブ確認間隔（秒）


def get_removable_drives() -> set[str]:
    """現在接続されているリムーバブルドライブのパス一覧を返す（Windows/Mac共通）。"""
    import platform
    drives = set()
    system = platform.system()

    for partition in psutil.disk_partitions(all=False):
        opts = partition.opts.lower()
        mountpoint = partition.mountpoint

        if system == "Windows":
            # Windows: opts に "removable" が含まれるか FAT系ファイルシステム
            is_removable = (
                "removable" in opts
                or partition.fstype.upper() in ("FAT", "FAT32", "EXFAT")
            )
        else:
            # Mac: リムーバブルドライブは /Volumes/ 以下にマウントされる
            # /Volumes/Macintosh HD など内蔵ドライブを除外するため local フラグを確認
            is_removable = (
                mountpoint.startswith("/Volumes/")
                and mountpoint != "/Volumes/"
                and "local" not in opts
            )

        if is_removable:
            try:
                psutil.disk_usage(mountpoint)
                drives.add(mountpoint)
            except (PermissionError, OSError):
                pass
    return drives


def should_process_drive(drive: str) -> bool:
    """このドライブを処理対象にするか判定する。"""
    if not RECORDER_DRIVE:
        return True  # 設定なし → 全リムーバブルドライブを対象
    # ドライブ文字の正規化（E:\ と E:/ と E: を同一視）
    normalize = lambda d: d.rstrip("/\\").upper().rstrip(":")
    return normalize(drive) == normalize(RECORDER_DRIVE)


def run_file_mover(drive: str):
    """file_mover.py を呼び出す。"""
    script_dir = Path(__file__).parent
    file_mover = script_dir / "file_mover.py"
    print(f"  file_mover.py を実行: {drive}")
    result = subprocess.run([sys.executable, str(file_mover), drive])
    if result.returncode == 0:
        print("  ✅ 処理完了")
    else:
        print(f"  ❌ 処理失敗 (終了コード: {result.returncode})")


def watch_loop():
    """ドライブ挿抜を監視するメインループ。"""
    print("AppLaud USB監視を開始しました。Ctrl+C で停止。")
    if RECORDER_DRIVE:
        print(f"監視対象ドライブ: {RECORDER_DRIVE}")
    else:
        print("監視対象ドライブ: 全リムーバブルドライブ（config.pyのRECORDER_DRIVEで絞り込み可能）")

    known_drives = get_removable_drives()
    if known_drives:
        print(f"起動時に検出済みドライブ: {', '.join(sorted(known_drives))}")
    else:
        print("起動時に検出済みドライブ: (なし)")

    while True:
        try:
            current_drives = get_removable_drives()
            new_drives = current_drives - known_drives

            for drive in sorted(new_drives):
                print(f"\n[{time.strftime('%H:%M:%S')}] 新しいドライブを検出: {drive}")
                if should_process_drive(drive):
                    run_file_mover(drive)
                else:
                    print(f"  スキップ（対象外ドライブ）")

            known_drives = current_drives
            time.sleep(POLL_INTERVAL_SEC)

        except KeyboardInterrupt:
            print("\n監視を停止しました。")
            break
        except Exception as e:
            print(f"エラー: {e}")
            time.sleep(POLL_INTERVAL_SEC)


def run_once():
    """現在接続中のリムーバブルドライブを一度だけ処理する（手動実行用）。"""
    print("接続中のリムーバブルドライブを確認します...")
    drives = get_removable_drives()
    if not drives:
        print("リムーバブルドライブが見つかりませんでした。")
        return
    for drive in sorted(drives):
        print(f"ドライブ: {drive}")
        if should_process_drive(drive):
            run_file_mover(drive)
        else:
            print(f"  スキップ（対象外ドライブ）")


def main():
    if "--once" in sys.argv:
        run_once()
    else:
        watch_loop()


if __name__ == "__main__":
    main()
