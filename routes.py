from datetime import timedelta
from flask import Blueprint, request, Response
from loguru import logger
from database import store
from api_requsets import ApiRequests
from texts import (
                    hello_text,
                    first_var_text,
                    second_var_text,
                    third_var_text,
                    tg_message_text
                    )
# from asyncio import sleep as asleep
from bot import send_tg_message
from config import MY_USER_ID

router = Blueprint('route', __name__)


@router.route("/avito_events", methods=["POST"])
def event_handler():
    data = request.json
    chat_id = data["payload"]["value"]["chat_id"]
    user_id = data["payload"]["value"]["user_id"]
    api = ApiRequests()
    step = store.get(chat_id)
    logger.error(request.json)
    if user_id == data["payload"]["value"]["author_id"]:
        return Response(status=200)

    if store.get(data["id"]):
        return Response(status=200)

    if step is None:
        api.send_message(hello_text, chat_id, user_id)
        username, user_url = api.get_user_info(chat_id)
        if data["payload"]["value"]["chat_type"] == "u2i":
            item_id = data["payload"]["value"]["item_id"]
            item_link = api.get_item_info(MY_USER_ID, item_id)
            send_tg_message(tg_message_text(username, user_url, item_link))
        else:
            send_tg_message(tg_message_text(username, user_url))
        store.set(chat_id, "1")

    else:
        message = data["payload"]["value"]["content"]["text"]
        logger.debug(message)
        
        if step == b"1":
            match message:
                case "1":
                    if store.get(f"{chat_id}:m1") is None:
                        api.send_message(first_var_text, chat_id, user_id)
                        store.set(f"{chat_id}:m1", "sended")
                case "2":
                    if store.get(f"{chat_id}:m2") is None:
                        api.send_message(second_var_text, chat_id, user_id)
                        store.set(f"{chat_id}:m2", "sended")
                case "3":
                    if store.get(f"{chat_id}:m3") is None:
                        api.send_message(third_var_text, chat_id, user_id)
                        store.set(f"{chat_id}:m3", "sended")
            # store.set(chat_id, "3")
    store.set(data["id"], "used")
    return "Ok"

# 0 - пользователь написал первое сообщение
# 1 - бот предложил пользователю варианты
# 2 - пользователь выбрал вариант
# 3 - бот отправил финальное сообщение
# 4 - пользователь написал еще одно сообщения после цикла бота 