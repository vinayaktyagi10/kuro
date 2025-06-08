#mistral_agent.py

import requests
import os
import json

OLLAMA_URL="http://localhost:11434/api/chat"
HISTORY_FILE=os.path.expanduser("~/.kuro_history.json")

def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE) as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
    return []

def save_history(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)

def ask_mistral(prompt, history=None):
    if history is None:
        history=[]

    messages = history +[{"role": "user", "content": prompt}]
    payload={
        "model":"mistral",
        "messages":messages,
        "stream":False
    }

    try:
        response=requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        res_json=response.json()
        content=res_json['message']['content']
        new_history=messages+[{"role": "assistant", "content": content}]
        save_history(new_history)
        return content, new_history
    except requests.RequestException as e:
        return f"Connection error: {e}", history
