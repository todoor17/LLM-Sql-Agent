import os
from gtts import gTTS


def clear_dir(dir_path):
    for item in os.listdir(dir_path):
        item_path = os.path.join(dir_path, item)
        os.remove(item_path)


def text_to_speech(text, current_time):
    print("here")
    clear_dir(r"D:\Projects\PythonProjects\QueryMate\frontend\public\audio")

    tts = gTTS(text=text, lang='en')
    path = f"D:/Projects/PythonProjects/QueryMate/frontend/public/audio/response{current_time}.mp3"
    tts.save(path)

    return_path = f"/audio/response{current_time}.mp3"
    return return_path

