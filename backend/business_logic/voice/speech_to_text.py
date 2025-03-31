import whisper

recognition_model = whisper.load_model("small")

def speech_to_text(file):
    result = recognition_model.transcribe(file, language="ro", fp16=False)
    return result["text"]
