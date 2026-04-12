import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("ZERNIO_API_KEY")


def get_live_reviews(profile_id, limit=1):
    url = "https://zernio.com/api/v1/inbox/reviews"

    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }

    params = {
        "accountId": profile_id,
        "limit": limit
    }

    response = requests.get(url, headers=headers, params=params)

    print("RAW API RESPONSE:")
    print(response.json())

    return response.json()