import os
import time
from gtts import gTTS


def clear_dir(dir_path):
    for item in os.listdir(dir_path):
        item_path = os.path.join(dir_path, item)
        os.remove(item_path)


def text_to_speech(text, state):
    clear_dir(r"D:\PythonProjects\SQL_Agent\backend\data\audio")
    hms = time.ctime().split(" ")[3].split(":")
    filename = f"result{hms[0]}{hms[1]}{hms[2]}.mp3"

    tts = gTTS(text=text, lang='en')

    path = f"D:/PythonProjects/SQL_Agent/backend/data/audio/{filename}"
    tts.save(path)
    state = path
    return filename
