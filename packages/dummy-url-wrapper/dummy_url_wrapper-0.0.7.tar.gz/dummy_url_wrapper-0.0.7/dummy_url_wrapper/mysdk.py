import os
import requests
from dotenv import load_dotenv
import json

load_dotenv()


def get_env_variable(variable_name, environment):
    return os.environ.get(f"{variable_name}_{environment.upper()}")


class URLWrapperClass:
    def __init__(self) -> None:
        self.variable_name = "ISSUANCE_URL"

    def getCardDetails(self, config=None, payload=None):
        card_id = payload["cardId"]
        token = config["token"]
        if token == "":
            return {"message": "Unauthorized"}
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer{token}",
        }
        requestOptions = {
            "headers": headers,
        }
        get_url = get_env_variable(self.variable_name, config["environment"])

        my_url = f"{get_url}/issuance/v1/cards/{card_id}"

        response = requests.get(my_url, **requestOptions)
        response_data = {"response": response.json()}
        return response_data

    def getCardHolderStatus(self, config=None, payload=None):
        mobileNo = payload["mobileNo"]
        token = config["token"]
        if token == "":
            return {"message": "Unauthorized"}
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer{token}",
        }
        requestOptions = {
            "headers": headers,
        }
        get_url = get_env_variable(self.variable_name, config["environment"])
        my_url = f"{get_url}/issuance/v1/cardholders/{mobileNo}"

        response = requests.get(my_url, **requestOptions)
        response_data = {"response": response.json()}
        return response_data

    def loadFundToCard(self, config=None, payload=None):
        try:
            token = config["token"]
            if token == "":
                return {"message": "Unauthorized"}
            payload = payload
            if not config["environment"] or not config["token"]:
                raise Exception("Config is not provided")

            if not payload:
                raise Exception("Payload body is not provided")

            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer{token}",
            }

            requestOptions = {"headers": headers, "data": json.dumps(payload)}
            get_url = get_env_variable(self.variable_name, config["environment"])

            my_url = f"{get_url}/issuance/v1/card/load"

            response = requests.post(my_url, **requestOptions)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as error:
            error_message = (
                f"HTTP Error: {error.response.status_code} - {error.response}"
            )
            return error_message
        except Exception as error:
            return str(error)

    def cardLockOrUnlock(self, config=None, payload=None):
        try:
            token = config["token"]
            if token == "":
                return {"message": "Unauthorized"}
            payload = payload
            if not config["environment"] or not config["token"]:
                raise Exception("Config is not provided")

            if not payload:
                raise Exception("Payload body is not provided")

            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer{token}",
            }

            requestOptions = {"headers": headers, "data": json.dumps(payload)}
            get_url = get_env_variable(self.variable_name, config["environment"])

            my_url = f"{get_url}/issuance/v1/card/lock"

            response = requests.put(my_url, **requestOptions)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as error:
            error_message = (
                f"HTTP Error: {error.response.status_code} - {error.response}"
            )
            return error_message
        except Exception as error:
            return str(error)

    def addAddress(self, config=None, payload=None):
        try:
            token = config["token"]
            if token == "":
                return {"message": "Unauthorized"}
            payload = payload
            if not config["environment"] or not config["token"]:
                raise Exception("Config is not provided")

            if not payload:
                raise Exception("Payload body is not provided")

            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer{token}",
            }

            requestOptions = {"headers": headers, "data": json.dumps(payload)}
            get_url = get_env_variable(self.variable_name, config["environment"])

            my_url = f"{get_url}/issuance/v1/addresses"

            response = requests.post(my_url, **requestOptions)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as error:
            error_message = (
                f"HTTP Error: {error.response.status_code} - {error.response}"
            )
            return error_message
        except Exception as error:
            return str(error)


Card91BusinessSDK = URLWrapperClass()
