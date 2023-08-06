import os
from quart_redis import RedisHandler

from .redis import RedisBovinePubSub
from .queue import QueueBovinePubSub


def BovinePubSub(app):
    redis_url = os.environ.get("BOVINE_REDIS")

    if redis_url:
        app.config["REDIS_URI"] = redis_url
        RedisHandler(app)

        @app.before_serving
        async def configure_bovine_pub_sub_redis():
            app.config["bovine_pub_sub"] = RedisBovinePubSub()

    else:

        @app.before_serving
        async def configure_bovine_pub_sub_queues():
            app.config["bovine_pub_sub"] = QueueBovinePubSub()
