#mistral_agent.py

import requests
OLLAMA_URL="http://localhost:11434/api/chat"
def ask_mistral(prompt, history=None):
    if history is None:
        history=[]

    messages = history +[{"role": "user", "content": prompt}]
    payload={
        "model":"mistral",
        "messages":messages,
        "stream":False
    }
        
    response=requests.post(OLLAMA_URL, json=payload)

    if response.status_code==200:
        res_json = response.json()
        content=res_json['message']['content']
        return content, messages + [{"role": "assistant", "content": content}]
    else:
        return f"Error {response.status_code}: {response.text}", history
