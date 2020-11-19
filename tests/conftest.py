import json

import pytest

from aiohttp import web, test_utils

from aiosnow.client import Session
from aiosnow.models.common import BaseModel, fields
from aiosnow.request.response import Response


class TestModel(BaseModel):
    pass


TEST_TCP_ADDRESS = "127.0.0.1"


class TestClient(test_utils.TestClient):
    def __init__(self, *args, **kwargs):
        super(TestClient, self).__init__(*args, **kwargs)
        self._session = Session(**kwargs)


@pytest.fixture
def aiosnow_client(loop):  # type: ignore
    """Factory to create a TestClient instance.

    aiohttp_client(app, **kwargs)
    aiohttp_client(server, **kwargs)
    aiohttp_client(raw_server, **kwargs)
    """
    clients = []

    async def go(app, server_kwargs=None, **kwargs):  # type: ignore
        server_kwargs = server_kwargs or {}

        server = test_utils.TestServer(app, loop=loop, **server_kwargs)
        client = TestClient(server, loop=loop, **kwargs)

        await client.start_server()
        clients.append(client)
        return client

    yield go

    async def finalize():  # type: ignore
        while clients:
            await clients.pop().close()

    loop.run_until_complete(finalize())


@pytest.fixture
def mock_error():
    def go(message, status, detail=None):
        return (
            dict(error=dict(message=message, detail=detail,), status="failure"),
            status,
        )

    yield go


@pytest.fixture
def mock_app():
    def go(method, path, content, status):
        async def handler(_):
            return web.Response(
                text=json.dumps(content), content_type="application/json", status=status
            )

        app = web.Application()
        app.router.add_route(method, path, handler)
        return app

    yield go


@pytest.fixture
def mock_session(aiosnow_client, mock_app):
    async def go(server_method="GET", server_path="/", content="", status=0):
        app = mock_app(server_method, server_path, content, status)
        client = await aiosnow_client(
            app, server_kwargs={"skip_url_asserts": True}, response_class=Response,
        )
        return client

    yield go


@pytest.fixture
def mock_field():
    def go(cls, name, **kwargs):
        field = cls(**kwargs)
        field.name = name
        return field

    yield go


@pytest.fixture
def mock_datetime_field(mock_field):
    def go(name, **kwargs):
        return mock_field(fields.DateTime, name, **kwargs)

    yield go


@pytest.fixture
def mock_boolean_field(mock_field):
    def go(name, **kwargs):
        return mock_field(fields.Boolean, name, **kwargs)

    yield go


@pytest.fixture
def mock_string_field(mock_field):
    def go(name, **kwargs):
        return mock_field(fields.String, name, **kwargs)

    yield go


@pytest.fixture
def mock_stringmap_field(mock_field):
    def go(name, **kwargs):
        return mock_field(fields.StringMap, name, **kwargs)

    yield go


@pytest.fixture
def mock_integer_field(mock_field):
    def go(name, **kwargs):
        return mock_field(fields.Integer, name, **kwargs)

    yield go


@pytest.fixture
def mock_integermap_field(mock_field):
    def go(name, **kwargs):
        return mock_field(fields.IntegerMap, name, **kwargs)

    yield go
