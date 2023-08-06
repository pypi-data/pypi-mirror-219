import pytest

from quart import Quart, make_response
from . import BovinePubSub


@pytest.fixture
async def test_app():
    app = Quart(__name__)
    BovinePubSub(app)

    @app.get("/")
    async def event_stream():
        pub_sub = app.config["bovine_pub_sub"]

        response = await make_response(
            pub_sub.event_stream("channel:test"),
            {
                "Content-Type": "text/event-stream",
                "Cache-Control": "no-cache",
                "Transfer-Encoding": "chunked",
            },
        )
        response.timeout = None

        return response

    async with app.test_app() as my_app:
        my_app.config = app.config
        yield my_app


async def test_event_source(test_app):
    async with test_app.test_client() as client:
        async with client.request("/") as connection:
            await test_app.config["bovine_pub_sub"].send("channel:test", b"test")

            data = await connection.receive()

            assert data == b"test"

            await connection.disconnect()
