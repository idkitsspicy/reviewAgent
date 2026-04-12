import json
import requests
import os

USE_MOCK = True

def get_reviews(access_token=None, location_id=None):
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, "mock_reviews.json")

    with open(file_path, "r", encoding="utf-8") as f:
        return {"reviews": json.load(f)}

    url = f"https://mybusiness.googleapis.com/v4/accounts/{location_id}/reviews"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    res = requests.get(url, headers=headers)
    return res.json()