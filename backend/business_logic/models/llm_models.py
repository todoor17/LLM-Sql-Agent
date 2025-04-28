import time

import ollama
from langchain_ollama import ChatOllama

llama = ChatOllama(model="llama3.2")

deepseek = ChatOllama(model="deepseek-r1")


def askDeepseek(prompt: str) -> str:
    start = time.time()
    response = ollama.chat(
        model="deepseek-r1",
        messages=[{"role": "user", "content": prompt}],
        options={
            "temperature": 0.7,
            "top_p": 0.9,
            "repeat_penalty": 1.1,
            "num_ctx": 4096,
            "num_predict": 4096,
            "num_gpu": 35,
        }
    )
    end = time.time()
    print(f"--------------------{end-start}-----------------------------------")
    return response["message"]["content"]


def askMistral(prompt: str) -> str:
    start = time.time()
    response = ollama.chat(
        model="mistral-nemo",
        messages=[{"role": "user", "content": prompt}],
        options={
            "num_gpu": 35,
        }
    )
    end = time.time()
    print(f"--------------------{end-start}------------------------------------")
    return response["message"]["content"]

def ask_sql_coder(prompt: str) -> str:
    start = time.time()
    response = ollama.chat(
        model="hf.co/defog/sqlcoder-7b-2:Q5_K_M",
        messages=[{"role": "user", "content": prompt}],
        options={
            "temperature": 0.7,
            "top_p": 0.9,
            "repeat_penalty": 1.1,
            "num_ctx": 4096,
            "num_predict": 4096,
            "num_gpu": 35,
        }
    )
    end = time.time()
    print(f"--------------------{end - start}------------------------------------")
    print(response["message"]["content"])
    return response["message"]["content"]