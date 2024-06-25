from .api_requsets import ApiRequests
from flask import Flask, request
from loguru import logger
from .routes import router

app = Flask(__name__)
app.register_blueprint(router)
api = ApiRequests()
api.webhooks_subscribe()
