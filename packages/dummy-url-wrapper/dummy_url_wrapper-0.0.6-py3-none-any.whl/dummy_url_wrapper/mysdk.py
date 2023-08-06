import os
import requests
from dotenv import load_dotenv

load_dotenv()

test_url = os.getenv("TEST_URL")
test_url_2 = os.getenv("TEST_URL_2")


class URLWrapperClass:
    def wrap_url(config, payload):
        card_id = payload["cardId"]
        config_data = config
        token = config_data["token"]
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer{token}",
        }
        requestOptions = {
            "headers": headers,
        }

        my_url = f"{test_url_2}/issuance/v1/cards/{card_id}"

        response = requests.get(my_url, **requestOptions)
        response.raise_for_status()
        response_data = {
            "response": response.json(),
            "config": config_data,
            "payload": payload,
        }
        return response_data
