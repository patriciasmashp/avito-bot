from flask import json
from config import CLIENT_ID, TOKEN, SERVER_URL, MY_USER_ID
import requests
from logging import debug


class ApiRequests:
    def __init__(self) -> None:
        self.bearer_token, self.expire_token = self.login()


    def login(self):
        data = {
            "client_id": CLIENT_ID,
            "client_secret": TOKEN,
            "grant_type": "client_credentials"
        }
        response = requests.post(
            "https://api.avito.ru/token",
            data,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
            ).json()
        return (response["access_token"], response["expires_in"])

    def webhooks_subscribe(self):
        url = "https://api.avito.ru/messenger/v3/webhook"

        payload = json.dumps({"url": SERVER_URL + "/avito_events"})
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.bearer_token}"
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        if response.status_code == 200:
            return True
        else:
            logger.error("Ошибка получения подписки на webhooks")
            logger.error(response.status_code)
            return False

    def send_message(self, text, chat_id, user_id):
        url = f"https://api.avito.ru/messenger/v1/accounts/{user_id}/chats/{chat_id}/messages"

        payload = json.dumps(
            {
                "message": {
                    "text": text
                },
                "type": "text"
            })
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {self.bearer_token}"
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        if response.status_code == 200:
            return True
        else:
            logger.error("Ошибка отправки сообщения")
            return False

    def get_item_info(self, user_id, item_id):
        url = f"https://api.avito.ru/core/v1/accounts/{user_id}/items/{item_id}/"

        headers = {
            'Authorization': f"Bearer {self.bearer_token}"
        }

        response = requests.request("GET", url, headers=headers)

        if response.status_code == 200:
            return response.json()["url"]
        else:
            logger.error("Ошибка получения ссылка на товар")
            return False

    def get_user_info(self, chat_id):
        url = f"https://api.avito.ru/messenger/v2/accounts/{MY_USER_ID}/chats/{chat_id}"

        headers = {
            'Authorization': f"Bearer {self.bearer_token}"
        }

        response = requests.request("GET", url, headers=headers)
        data = response.json()
        
        for user in data["users"]:
            if user["id"] != MY_USER_ID:
                
                return (user["name"], user["public_user_profile"]["url"])
