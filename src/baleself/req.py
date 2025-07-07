import requests

def req(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response
    else:
        return f"{response.status_code} | cannot give content from daradegeapi."


def baleinfo(uinfo):
    it_response = req(f'https://api.daradege.ir/bale_id_data?username={uinfo}')
    it_response = it_response.json()
    return (f"🔰*name*: {str(it_response['name'])} 👀*description*: {str(it_response['description'])} 🤖*bot*: {str(it_response['is_bot'])} * 🆔*user id*: {str(it_response['user_id'])}")

response = requests.get("https://api.daradege.ir/bale_id_data?username=@9044395749")
print(response.json()["status"])