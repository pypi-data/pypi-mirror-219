import requests
import json
import mutual

def clear(bot_id):
    url = f"https://api-agent.mutuai.io/api/clear/{bot_id}"
    headers = {
        "Authorization": f"Bearer {mutual.api_key}"
    }
    response = requests.get(url, headers=headers)

    if response.status_code < 300:
        response_json = response.json()
        return response_json
    else:
        return {
            "details":f"Request failed with status code {response.status_code}, with an Error Message: {json.loads(response.text)['detail'] or response.text}"
        }