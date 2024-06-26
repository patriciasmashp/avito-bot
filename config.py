from dotenv import load_dotenv
import os
load_dotenv()

TOKEN = os.environ["AVITO_TOKEN"]
CLIENT_ID = os.environ["AVITO_CLIENT_ID"]
API_URL = "https://api.avito.ru"
SERVER_URL = os.environ["SERVER_URL"]
REDIS_RUL = os.environ["REDIS_URL"]
TG_TOKEN = os.environ["TG_TOKEN"]
MY_USER_ID = os.environ["MY_USER_ID"]
TG_CHAT_ID = os.environ["TG_CHAT_ID"]