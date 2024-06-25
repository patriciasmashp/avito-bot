import telebot
from config import TG_TOKEN, TG_CHAT_ID

def send_tg_message(text):
    bot = telebot.TeleBot(TG_TOKEN)
    chat_id = TG_CHAT_ID
    bot.send_message(chat_id, text, parse_mode="Markdown")