import requests
import os
from dotenv import load_dotenv
import time

url_base = "https://www.robotevents.com/api/v2"

load_dotenv()
token = os.environ.get("ACCESS_TOKEN")
auth_key = "Bearer " + token

headers = {
    "accept": "application/json",
    "Authorization": auth_key
}

def fetch_data(item, query):
    params = query

    current_page = 1
    all_data = []
    
    while True:
        url_suffix = f"/{item}?per_page=250&page={str(current_page)}"
        endpoint = url_base + url_suffix

        response = requests.get(endpoint, headers=headers, params=params)
        data = response.json()
        all_data.extend(data["data"])

        if current_page >= data["meta"]["last_page"]:
            break

        current_page += 1
        time.sleep(1)

    return all_data