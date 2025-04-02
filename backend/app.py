import os
from queue import Queue
from flask import Flask, request, jsonify
from flask_cors import CORS
from business_logic.agents.llm_sql_agent import graph, queue
from business_logic.voice.speech_to_text import speech_to_text
from data.db_data import db_info


app = Flask(__name__)
CORS(app)

initial_state = {
    "database_info": db_info,
    "type": "",
    "answer": "",
    "status": "",
    "correct": False,
    "suggested_new_query": "",
    "all_fields_present": True,
    "missing_fields": "",
    "prompt": "",
    "sql_answer": "",
    "insert_status": ""
}


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route("/get_audio", methods=["POST"])
def get_audio():
    recordings_dir = f"{app.root_path}/data/audio"

    prompt_file = request.files["file"]
    prompt_path = os.path.join(recordings_dir, "recording.wav")
    prompt_file.save(prompt_path)

    text = speech_to_text(prompt_path)
    queue.put(text)

    graph.invoke(initial_state)

    return jsonify({"answer": initial_state["sql_answer"]})


if __name__ == '__main__':
    app.run()
