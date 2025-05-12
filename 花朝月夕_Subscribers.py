import json
import os

def save_Ssubcribers(user_id_list):
    FILE_PATH = 'Sah_Yang_subs.json'
    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        json.dump(list(user_id_list), f)
def load_Ssubcribers():
    FILE_PATH = 'Sah_Yang_subs.json'
    if not os.path.exists(FILE_PATH):
        return set()
    with open(FILE_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return set(data)

def save_CHsubcribers(user_id_list):
    FILE_PATH = 'leechunhyang.subs.json'
    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        json.dump(list(user_id_list), f)
def load_CHsubcribers():
    FILE_PATH = 'leechunhyang.subs.json'
    if not os.path.exists(FILE_PATH):
        return set()
    with open(FILE_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return set(data)

def save_cz_subcribers(user_id_list):
    FILE_PATH = 'chyeonz_.subs.json'
    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        json.dump(list(user_id_list), f)
def load_cz_subcribers():
    FILE_PATH = 'chyeonz_.subs.json'
    if not os.path.exists(FILE_PATH):
        return set()
    with open(FILE_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return set(data)

def save_ao_subcribers(user_id_list):
    FILE_PATH = 'ao_o5.subs.json'
    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        json.dump(list(user_id_list), f)
def load_ao_subcribers():
    FILE_PATH = 'ao_o5.subs.json'
    if not os.path.exists(FILE_PATH):
        return set()
    with open(FILE_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return set(data)