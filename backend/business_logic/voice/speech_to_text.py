import whisper

recognition_model = whisper.load_model("medium")

def speech_to_text(file):
    result = recognition_model.transcribe(file, language="en", fp16=False)
    return result["text"]

# print(speech_to_text(r"D:\Projects\PythonProjects\QueryMate\backend\data\audio\en_voice_sample.wav"))

# import json
# import subprocess
# import vosk
# import wave
#
# model_path = r"D:\Projects\PythonProjects\QueryMate\backend\business_logic\models\voice_model\vosk-model-en-us-0.22"
# audio_model = vosk.Model(model_path)
#
#
# def convert_to_wav(input_path, output_path):
#     subprocess.run([
#         "ffmpeg", "-y", "-i", input_path,
#         "-ac", "1",             # mono
#         "-ar", "16000",         # 16kHz
#         "-sample_fmt", "s16",   # 16-bit signed PCM
#         output_path
#     ], check=True)
#
#
# def transcribe(path):
#     with wave.open(path, "rb") as wf:
#         recognizer = vosk.KaldiRecognizer(audio_model, wf.getframerate())
#         while True:
#             data = wf.readframes(4000)
#             if len(data) == 0:
#                 break
#             recognizer.AcceptWaveform(data)
#
#     result = recognizer.FinalResult()
#     result_dict = json.loads(result)
#
#     return result_dict.get("text")

