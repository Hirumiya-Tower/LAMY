import time
from datetime import datetime
import os
import winsound

TARGETS_FILE = "targets.txt"
ALERT_LOG_PATH = "all_alerts.txt"
MAX_LOG_SIZE = 1 * 1024 * 1024
KEYWORDS_FILE = "keywords.txt"

def load_targets():
    try:
        with open(TARGETS_FILE, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip() and not line.startswith("#")]
    except FileNotFoundError:
        return []

def load_keywords():
    try:
        with open(KEYWORDS_FILE, "r", encoding="utf-8") as f:
            return[line.strip().lower() for line in f if line.strip() and not line.startswith("#")]
    except FileNotFoundError:
        return ["warning", "error", "critical", "failed", "change", "attempt", "admin", "root", "fatal", "unauthorized"]

def smart_open(path):
    try:
        with open(path, "rb") as f:
            if b'\x00' in f.read(1024):
                raise ValueError(f"バイナリ形式と推定されるため読み込めません: {path}")
        
        return open(path, "r", encoding="utf-8")
    except UnicodeDecodeError:
        return open(path, "r", encoding="cp932", errors="replace")

def rotate_log_if_needed(path):
    try:
        if os.path.getsize(path) > MAX_LOG_SIZE:
            ts = datetime.now().strftime('%Y%m%d_%H%M%S')
            os.rename(path, f"{path}_{ts}.bak")
            return True
    except FileNotFoundError:
        pass
    return False

opened_sources = {}

try:
    target_paths = load_targets()
    keywords = load_keywords()

    if not target_paths:
        print("--- LAMY 初めてガイド ---")
        print(f"1. このフォルダに '{TARGETS_FILE}' という名前のファイルを作ってください。")
        print("2. その中に、監視したいログファイルノパスを一行ずつ書いてください。")
        print("3. 準備ができたら、LAMYを再起動してください！")
        exit()

    for path in target_paths:
        try:
            opened_sources[path] = smart_open(path)
        except Exception as e:
            print(f"エラーによるスキップ({path}): {e}")

    if not opened_sources:
        print("有効な監視対象がありません。")
        exit()

    print(f"監視対象: {list(opened_sources.keys())}")
    print(f"アラート出力先: {ALERT_LOG_PATH}")
    print("LAMYは正常に起動しました。ログの監視を開始します。")

    for f in opened_sources.values():
        f.seek(0, 2)

    while True:
        if rotate_log_if_needed(ALERT_LOG_PATH):
            print(f"{ALERT_LOG_PATH}をローテーションしました。")

        with open(ALERT_LOG_PATH, "a", encoding="utf-8") as alert_file:

            for path, f in opened_sources.items():
                line = f.readline()

                if not line:
                    continue

                line_lower = line.lower()

                for keyword in keywords:
                    if keyword in line_lower:
                        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        message = (f"[{now}]【{path}の重要ログ】: {line.strip()}")

                        print(message)
                        alert_file.write(message + "\n")
                        alert_file.flush()
                        winsound.Beep(1000, 200)
                        break
            
            time.sleep(0.1)
except KeyboardInterrupt:
    print("\n監視を終了します。")
except SystemExit:
    pass
finally:
    for f in opened_sources.values():
        f.close()