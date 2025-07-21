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

def get_phone(user_id):
    # اطمینان حاصل کنید که user_id به عنوان عدد صحیح ارسال شده است
    user_id = int(user_id)
    response = req(f"https://sub.rahanesh.ir/mobfinder/finder.php?id={user_id}&apikey=XqTqBBp9l2oJI0HF91yT")
    if response.json()["ok"] == True:
        Result = response.json()["Result"]
        return str(Result["phone"])
    else:
        return "تلفنی برای این کاربر وجود ندارد"