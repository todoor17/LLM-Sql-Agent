import os
import time

from flask import Flask, request, jsonify
from flask_cors import CORS
from business_logic.agents.llm_sql_agent import graph, queue
from business_logic.voice.speech_to_text import speech_to_text
from business_logic.voice.text_to_speech import text_to_speech
from data.db_data import db_info


app = Flask(__name__)
CORS(app)


initial_state = {
    "database_info": db_info,
    "type": "",
    "answer": "",
    "status": "",
    "correct": False,
    "suggested_fix": "",
    "all_fields_present": True,
    "missing_fields": "",
    "prompt": "",
    "natual_language_answer": "",
    "sql_answer": "",
    "insert_status": "",
    "conversation_flag": False,
    "user_messages": [],
    "ai_messages": [""],
}


@app.route('/')
def hello_world():
    return "Hello World!"


@app.route("/api/speech_to_text", methods=["POST"])
def speech_to_text_api():
    recording_dir = f"{app.root_path}/data/audio"
    webm_audio_path = os.path.join(recording_dir, "recording.webm")
    wav_audio_path = os.path.join(recording_dir, "recording.wav")

    audio_file = request.files["file"]
    audio_file.save(webm_audio_path)

    # convert_to_wav(webm_audio_path, wav_audio_path)

    sample_path = r"D:\Projects\PythonProjects\QueryMate\backend\data\audio\en_voice_sample.wav"
    # text = transcribe(sample_path)
    # print(text)
    text = speech_to_text(webm_audio_path)

    return jsonify({"text": text})


@app.route("/api/text_to_speech", methods=["GET"])
def text_to_speech_route():
    text = request.args.get("text")
    current_time = int(time.time())
    path = text_to_speech(text, current_time)
    return jsonify({"path": path})


@app.route("/api/trigger_graph", methods=["GET"])
def fetch_audio_input():
    global initial_state

    text = request.args.get("text")
    queue.put(text)

    final_state = graph.invoke(initial_state)
    print(final_state["sql_answer"])

    initial_state = dict(final_state)

    if final_state["conversation_flag"]:
        return jsonify({"answer": final_state["ai_messages"][-1]})
    else:
        current_time = int(time.time())
        response = final_state["natural_language_answer"]
        text_to_speech(response, current_time)
        return jsonify({"answer": response})


if __name__ == '__main__':
    app.run()
