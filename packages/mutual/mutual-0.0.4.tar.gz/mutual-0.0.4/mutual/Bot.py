import requests
import json
import mutual

def getBot(limit=20, offset=0):
    url = f"https://api-agent.mutuai.io/api/bots?limit={limit}&offset={offset}"
    headers = {
        "Authorization": f"Bearer {mutual.api_key}"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise an exception if the response contains an HTTP error status code
    return response.json()

def getBots(bot_id):
    url = f"https://api-agent.mutuai.io/api/bots/{str(bot_id)}"
    headers = {
        "Authorization": f"Bearer {mutual.api_key}"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise an exception if the response contains an HTTP error status code
    return response.json()

def createBot(bot_id, bot_name, bot_org):
    url = "https://api-agent.mutuai.io/api/bots"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {mutual.api_key}"
    }
    data = {
        "bot_id": str(bot_id),
        "bot_name": bot_name,
        "bot_org": bot_org
    }
    response = requests.post(url, data=json.dumps(data), headers=headers)
    response.raise_for_status()  # Raise an exception if the response contains an HTTP error status code
    return response.json()

def updateBot(bot_id, bot_name=None, bot_org=None):
    url = f"https://api-agent.mutuai.io/api/bots/{str(bot_id)}"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {mutual.api_key}"
    }
    data = {
        "bot_name": bot_name,
        "bot_org": bot_org
    }
    # remove keys with None value
    data = {k: v for k, v in data.items() if v is not None}
    response = requests.patch(url, data=json.dumps(data), headers=headers)
    response.raise_for_status()  # Raise an exception if the response contains an HTTP error status code
    return response.json()
