import os
from gtts import gTTS


def clear_dir(dir_path):
    for item in os.listdir(dir_path):
        item_path = os.path.join(dir_path, item)
        os.remove(item_path)


def text_to_speech(text):
    clear_dir("D:/PythonProjects/SQL_Agent/frontend/public/audio")

    tts = gTTS(text=text, lang='en')
    path = "D:/PythonProjects/SQL_Agent/frontend/public/audio/response.wav"
    tts.save(path)

    return path
