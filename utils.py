import requests
import json
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