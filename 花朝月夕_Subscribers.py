import json
import os

FILE_PATH = 'Sah_Yang_subs.json'

def save_Ssubcribers(user_id_list):
    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        json.dump(list(user_id_list), f)
def load_Ssubcribers():
    if not os.path.exists(FILE_PATH):
        return set()
    with open(FILE_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return set(data)