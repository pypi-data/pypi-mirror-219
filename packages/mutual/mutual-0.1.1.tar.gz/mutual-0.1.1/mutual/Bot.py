import requests
import json
import mutual

bot_default_response = {
            "bot_id": None,
            "bot_name": None,
            "bot_org": None,
            "bot_chat_index": None,
            "prompt_id": None,
            "details": None
        }

def get_bots(limit=20, offset=0):
    url = f"https://api-agent.mutuai.io/api/bots?limit={limit}&offset={offset}"
    headers = {
        "Authorization": f"Bearer {mutual.api_key}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code < 300:
        return response.json()
    else:
        bot_default_response["details"] = f"Request failed with status code {response.status_code}, with an Error Message: {json.loads(response.text)['detail'] or response.text}"
        return bot_default_response

def get_bot(bot_id):
    url = f"https://api-agent.mutuai.io/api/bots/{str(bot_id)}"
    headers = {
        "Authorization": f"Bearer {mutual.api_key}"
    }
    response = requests.get(url, headers=headers)
    # response.raise_for_status()  # Raise an exception if the response contains an HTTP error status code
    if response.status_code < 300:
        return response.json()
    else:
        bot_default_response["details"] = f"Request failed with status code {response.status_code}, with an Error Message: {json.loads(response.text)['detail'] or response.text}"
        return bot_default_response

def create_bot(bot_name, bot_org = "Mutual", prompt_id = "default"):
    url = "https://api-agent.mutuai.io/api/bots"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {mutual.api_key}"
    }
    data = {
        # "bot_id": str(bot_id),
        "bot_name": bot_name,
        "bot_org": bot_org,
        "prompt_id": prompt_id
    }
    response = requests.post(url, data=json.dumps(data), headers=headers)
    if response.status_code < 300:
        return response.json()
    else:
        bot_default_response["details"] = f"Request failed with status code {response.status_code}, with an Error Message: {json.loads(response.text)['detail'] or response.text}"
        return bot_default_response

def update_bot(bot_id, bot_name=None, bot_org=None, prompt_id=None):
    url = f"https://api-agent.mutuai.io/api/bots/{str(bot_id)}"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {mutual.api_key}"
    }
    data = {
        "bot_name": bot_name,
        "bot_org": bot_org,
        "prompt_id": prompt_id
    }
    # remove keys with None value
    data = {k: v for k, v in data.items() if v is not None}
    response = requests.patch(url, data=json.dumps(data), headers=headers)
    if response.status_code < 300:
        return response.json()
    else:
        bot_default_response["details"] = f"Request failed with status code {response.status_code}, with an Error Message: {json.loads(response.text)['detail'] or response.text}"
        return bot_default_response


class Bot:
    def __init__(self, api_key, bot_id=None, bot_name=None, prompt_id = "default"):
        self.api_key = api_key
        self.bot_id = bot_id
        self.bot_name = bot_name
        self.prompt_id = prompt_id

        self.default_stream_response = {
                        "error": None,
                        "status": None,
                        "content": None,
                        "bot_id": None,
                        "user_id": None,
                        "new_bot": None,
                        "new_bot_user": None,
                        "prompt_id": None
        }

    def updateBot(self, bot_name=None, bot_org=None, prompt_id=None):
        url = f"https://api-agent.mutuai.io/api/bots/{str(self.bot_id)}"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        data = {
            "bot_name": bot_name,
            "bot_org": bot_org,
            "prompt_id": prompt_id
        }
        # remove keys with None value
        data = {k: v for k, v in data.items() if v is not None}
        response = requests.patch(url, data=json.dumps(data), headers=headers)
        if response.status_code < 300:
            return response.json()
        else:
            self.default_stream_response["content"] = f"Request failed with status code {response.status_code}, with an Error Message: {json.loads(response.text)['detail'] or response.text}"
            return self.default_stream_response

    def chat(self, content, username=None, multiplayer_memory = True, context_window = 2):
        url = "https://api-agent.mutuai.io/api/chat"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        data = {
            "content": content,
            "bot_id": str(self.bot_id),
            "username": username,
            "prompt_id": self.prompt_id,
            "multiplayer": multiplayer_memory,
            "context_window": context_window
        }

        response = requests.post(url, data=json.dumps(data), headers=headers, stream=True)

        if response.status_code < 300:
            is_new_bot = False
            is_new_user = False
            for line in response.iter_lines():
                if line:  # filter out keep-alive new lines
                    json_data = json.loads(line)
                    if json_data['new_bot'] and not is_new_bot:
                        is_new_bot = True
                        print(f"Newly created bot! Here is your id: {json_data['bot_id']}")
                    if json_data['new_bot_user'] and not is_new_user:
                        is_new_user = True
                        print(f"New user {json_data['user_id']} created interacting with bot id: {json_data['bot_id']}")
                    if json_data['content'] =='[close]':
                        continue
                    yield json_data
        else:
            self.default_stream_response['content'] = f"Request failed with status code {response.status_code}, with an Error Message: {json.loads(response.text)['detail'] or response.text}"
            return self.default_stream_response
