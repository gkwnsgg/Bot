import os
import json

def Sah_load_last_video_id():
    FILE_PATH = 'Sah_last_video.json'
    if not os.path.exists(FILE_PATH):
        return None
    with open(FILE_PATH, 'r') as f:
        return json.load(f).get("videoId")
def Sah_save_last_video_id(video_id):
    FILE_PATH = 'Sah_last_video.json'
    with open(FILE_PATH, 'w') as f:
        json.dump({"videoId": video_id}, f)