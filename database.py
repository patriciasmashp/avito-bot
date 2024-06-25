import redis
from .config import REDIS_RUL


store = redis.Redis.from_url(REDIS_RUL)
