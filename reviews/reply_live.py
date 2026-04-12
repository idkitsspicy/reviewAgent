import os
import requests
from dotenv import load_dotenv
from urllib.parse import quote

load_dotenv()

API_KEY = os.getenv("ZERNIO_API_KEY")


def post_reply(review_id, account_id, message):
    encoded_review_id = quote(review_id, safe='')

    url = f"https://zernio.com/api/v1/inbox/reviews/{encoded_review_id}/reply"

    payload = {
        "accountId": account_id,
        "message": message
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    response = requests.post(url, json=payload, headers=headers)

    print("STATUS:", response.status_code)
    print("RAW RESPONSE:", response.text)

    try:
        return response.json()
    except:
        return {
            "status_code": response.status_code,
            "raw_response": response.text
        }