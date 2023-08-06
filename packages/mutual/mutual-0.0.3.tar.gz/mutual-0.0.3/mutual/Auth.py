import requests
import json
import mutual

def signup(user_id, email):
    url = "https://api-agent.mutuai.io/api/signup"
    data = {
        "user_id": user_id,
        "email": email
    }

    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.post(url, data=json.dumps(data), headers=headers)

    if response.status_code == 200:
        response_json = response.json()
        mutual.api_key = response_json.get('api_key') # save the api_key to config
        return response_json
    else:
        raise Exception(f"Request failed with status code {response.status_code}")
