import requests
import os
from dotenv import load_dotenv
import time

url_base = "https://www.robotevents.com/api/v2"

# Storage of RobotEvents API token/key in .env
load_dotenv()
token = os.environ.get("ACCESS_TOKEN")
auth_key = "Bearer " + token

# Standard headers for all requests; required
headers = {
    "accept": "application/json",
    "Authorization": auth_key
}

# Standard function for requesting data from RobotEvents API
def fetch_data(item, query):
    params = query

    current_page = 1
    all_data = []
    
    # API results are paginated; iterate through pages
    while True:
        url_suffix = f"/{item}?per_page=250&page={str(current_page)}"
        endpoint = url_base + url_suffix

        # Parameters provided when function called
        response = requests.get(endpoint, headers=headers, params=params)
        data = response.json()
        all_data.extend(data["data"])

        if current_page >= data["meta"]["last_page"]:
            break

        current_page += 1
        # Spread requests for multiple pages by 1 second
        time.sleep(1)

    return all_data