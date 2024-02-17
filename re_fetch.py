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


def fetch_teams(program):
    params = {
        "country": "GB",
        "program": [program],
        "registered": True
    }

    current_page = 1
    all_data = []

    url_suffix = "/teams"
    
    while True:
        url_suffix = "/teams?page=" + str(current_page)
        endpoint = url_base + url_suffix

        response = requests.get(endpoint, headers=headers, params=params)
        data = response.json()
        all_data.extend(data["data"])

        if current_page == data["meta"]["last_page"]:
            break

        current_page += 1
        time.sleep(1)

    return all_data


def fetch_events(season):
    params = {
        "region": "United Kingdom",
        "season": [season],
    }

    current_page = 1
    all_data = []

    url_suffix = "/events"

    while True:
        url_suffix = "/events?page=" + str(current_page)
        endpoint = url_base + url_suffix

        response = requests.get(endpoint, headers=headers, params=params)
        data = response.json()
        all_data.extend(data["data"])

        if current_page == data["meta"]["last_page"]:
            break

        current_page += 1
        time.sleep(1)

    return all_data