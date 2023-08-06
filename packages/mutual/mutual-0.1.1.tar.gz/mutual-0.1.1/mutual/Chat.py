import requests
import json
import mutual

default_stream_response = {
                        "error": None,
                        "status": None,
                        "content": None,
                        "bot_id": None,
                        "user_id": None,
                        "new_bot": None,
                        "new_bot_user": None,
                        "prompt_id": None
                        }

def create(content, bot_id=None, username=None, prompt_id=None, error_logs=False, multiplayer_memory = True, context_window = 2):
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
        "username": username,
        "prompt_id": prompt_id,
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
                if json_data['error'] is not None and not error_logs:
                    continue
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
        # raise Exception(f"Request failed with status code {response.status_code}, with an Error Message: {json.loads(response.text)['detail']}")
        default_stream_response['content'] = f"Request failed with status code {response.status_code}, with an Error Message: {json.loads(response.text)['detail'] or response.text}"
        return default_stream_response


def create_demo(content, error_logs=False, multiplayer_memory = True, context_window = 2):

    url = "https://api-agent.mutuai.io/api/test_chat"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {mutual.api_key}"
    }
    data = {
        "content": content,
        "multiplayer": multiplayer_memory,
        "context_window": context_window
    }

    response = requests.post(url, data=json.dumps(data), headers=headers, stream=True)

    if response.status_code < 300:
        for line in response.iter_lines():
            if line:  # filter out keep-alive new lines
                json_data = json.loads(line)
                if json_data['error'] is not None and not error_logs:
                    continue
                if json_data['content'] =='[close]':
                    continue
                yield json_data
    else:
        # raise Exception(f"Request failed with status code {response.status_code}, with an Error Message: {json.loads(response.text)['detail']}")
        default_stream_response['content'] = f"Request failed with status code {response.status_code}, with an Error Message: {json.loads(response.text)['detail'] or response.text}"
        return default_stream_response
