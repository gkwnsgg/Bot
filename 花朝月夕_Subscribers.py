import json
import os
import subprocess
from datetime import datetime

FILE_PATH = 'subs.json'
LOG_PATH = 'gitlog.txt'

def log_user_action(user_ids, action):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(LOG_PATH, 'a', encoding='utf-8') as log_file:
        for uid in user_ids:
            log_file.write(f"[{timestamp}] 사용자 {uid} {action}\n")

def save_subscribers(user_id_list, changed_ids=None, action=None):
    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        json.dump(list(user_id_list), f, ensure_ascii=False, indent=2)
    if changed_ids and action:
        log_user_action(changed_ids, action)
    try:
        subprocess.run(["git", "add", FILE_PATH], check=True)
        subprocess.run(["git", "commit", "-m", "자동 저장: subs.json 변경"], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Git 푸시 실패: {e}")
def load_subscribers():
    if not os.path.exists(FILE_PATH):
        return set()
    with open(FILE_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return set(data)