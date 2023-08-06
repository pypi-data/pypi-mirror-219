import requests
import json
import mutual

default_prompt_response = {
    "prompt_id": None,
    "identity_prompt": None,
    "backstory_prompt": None,
    "world_prompt": None,
    "action_prompt": None,
    "internal_thought": None,
    "external_thought": None,
    "internal_thought_memory": None,
    "external_thought_memory": None,
    "summarization_prompt": None,
    "details": "Successful"
}

def get_prompts(limit=20, offset=0):
    url = f"https://api-agent.mutuai.io/api/prompts?limit={limit}&offset={offset}"
    headers = {
        "Authorization": f"Bearer {mutual.api_key}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code < 300:
        return response.json()
    else:
        default_prompt_response["details"] = f"Request failed with status code {response.status_code}, with an Error Message: {json.loads(response.text)['detail'] or response.text}"
        return default_prompt_response

def get_prompt(prompt_id):
    url = f"https://api-agent.mutuai.io/api/prompts/{str(prompt_id)}"
    headers = {
        "Authorization": f"Bearer {mutual.api_key}"
    }
    response = requests.get(url, headers=headers)
    # response.raise_for_status()  # Raise an exception if the response contains an HTTP error status code
    if response.status_code < 300:
        return response.json()
    else:
        default_prompt_response["details"] = f"Request failed with status code {response.status_code}, with an Error Message: {json.loads(response.text)['detail'] or response.text}"
        return default_prompt_response

def create_prompt(
    prompt_id,
    identity_prompt=None,
    backstory_prompt=None,
    world_prompt=None,
    action_prompt=None,
    internal_thought=None,
    external_thought=None,
    internal_thought_memory=None,
    external_thought_memory=None,
    summarization_prompt=None
):
    url = f"https://api-agent.mutuai.io/api/prompts"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {mutual.api_key}"
    }
    data = {
        "prompt_id": prompt_id,
        "identity_prompt": identity_prompt,
        "backstory_prompt": backstory_prompt,
        "world_prompt": world_prompt,
        "action_prompt": action_prompt,
        "internal_thought": internal_thought,
        "external_thought": external_thought,
        "internal_thought_memory": internal_thought_memory,
        "external_thought_memory": external_thought_memory,
        "summarization_prompt": summarization_prompt
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code < 300:
        return response.json()
    else:
        default_prompt_response["details"] = f"Request failed with status code {response.status_code}, with an Error Message: {response.text}"
        return default_prompt_response

def update_prompt(prompt_id,
    identity_prompt=None,
    backstory_prompt=None,
    world_prompt=None,
    action_prompt=None,
    internal_thought=None,
    external_thought=None,
    internal_thought_memory=None,
    external_thought_memory=None,
    summarization_prompt=None):

    url = f"https://api-agent.mutuai.io/api/prompts/{str(prompt_id)}"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {mutual.api_key}"
    }
    data = {
        "identity_prompt": identity_prompt,
        "backstory_prompt": backstory_prompt,
        "world_prompt": world_prompt,
        "action_prompt": action_prompt,
        "internal_thought": internal_thought,
        "external_thought": external_thought,
        "internal_thought_memory": internal_thought_memory,
        "external_thought_memory": external_thought_memory,
        "summarization_prompt": summarization_prompt
    }

    # remove keys with None value
    data = {k: v for k, v in data.items() if v is not None}
    response = requests.patch(url, data=json.dumps(data), headers=headers)
    if response.status_code < 300:
        return response.json()
    else:
        default_prompt_response["details"] = f"Request failed with status code {response.status_code}, with an Error Message: {json.loads(response.text)['detail'] or response.text}"
        return default_prompt_response
