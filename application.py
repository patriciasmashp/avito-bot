from api_requsets import ApiRequests
from flask import Flask, request
from loguru import logger
from routes import router
import logging
from logging import FileHandler


app = Flask(__name__)
app.register_blueprint(router)
file_handler = FileHandler("errors.log")
file_handler.setLevel(logging.ERROR)
app.logger.addHandler(file_handler)

api = ApiRequests()
api.webhooks_subscribe()

