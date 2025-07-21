import requests
import json

def req(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response
    else:
        return f"{response.status_code} | cannot give content from daradegeapi."

def get_generated_text(prompt: str) -> str:
    url = 'https://text.pollinations.ai/'
    headers = {
        'Content-Type': 'application/json',
    }
    payload = {
        'messages': [
            {'role': 'user', 'content': prompt}
        ],
        'model': 'openai',
        'private': True
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    response.raise_for_status()
    return response.text
