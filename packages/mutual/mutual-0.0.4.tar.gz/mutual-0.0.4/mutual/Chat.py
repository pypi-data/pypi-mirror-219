import requests
import json
import mutual

def create(content, bot_id=None, username=None):
    if bot_id is None:
        bot_id = mutual.bot_id
    if bot_id is None:
        raise ValueError("bot_id must be provided either as argument or set in config")

    url = "https://api-agent.mutuai.io/api/chat"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {mutual.api_key}"
    }
    data = {
        "content": content,
        "bot_id": str(bot_id),
        "username": username
    }

    response = requests.post(url, data=json.dumps(data), headers=headers, stream=True)

    if response.status_code == 200:
        for line in response.iter_lines():
            if line:  # filter out keep-alive new lines
                yield json.loads(line)
    else:
        raise Exception(f"Request failed with status code {response.status_code}")


def create_demo(content):

    url = "https://api-agent.mutuai.io/api/test_chat"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {mutual.api_key}"
    }
    data = {
        "content": content
    }

    response = requests.post(url, data=json.dumps(data), headers=headers, stream=True)

    if response.status_code == 200:
        for line in response.iter_lines():
            if line:  # filter out keep-alive new lines
                yield json.loads(line)
    else:
        raise Exception(f"Request failed with status code {response.status_code}")