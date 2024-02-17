import requests
import os
from dotenv import load_dotenv

url_base = "https://www.robotevents.com/api/v2"
url_suffix = "/events"
endpoint = url_base + url_suffix

load_dotenv()
token = os.environ.get("ACCESS_TOKEN")
auth_key = "Bearer " + token

headers = {
    "accept": "application/json",
    "Authorization": auth_key
}

def fetch_test():
    params = {
        "region": "United Kingdom",
        "season": [181]
    }

    response = requests.get(endpoint, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None