import json

import pytest
from aiohttp import test_utils, web

from aiosnow.client import Client
from aiosnow.models import fields
from aiosnow.request.response import Response


class TestClient(Client):
    def __init__(self, server, **kwargs):
        self._server = server
        super(TestClient, self).__init__(address="", **kwargs)
        self.base_url = ""

    def get_session(self, *args, **kwargs):
        return test_utils.TestClient(
            self._server, *args, response_class=self.response_cls, **kwargs
        )


@pytest.fixture
def aiosnow_session(loop):  # type: ignore
    """Factory to create a

    Returns:
        Tuple(aiohttp.test_utils.TestServer, aiosnow.TestClient, aiohttp.TestClient)
    """

    sessions = []

    async def go(app, server_kwargs=None, **kwargs):  # type: ignore
        server_kwargs = server_kwargs or {}

        server = test_utils.TestServer(app, loop=loop, **server_kwargs)
        client = TestClient(
            server,
            basic_auth=("a", "b"),
            response_cls=kwargs.pop("response_cls", Response),
        )
        session = client.get_session(loop=loop, **kwargs)

        await session.start_server()
        sessions.append(session)
        return server, client, session

    yield go

    async def finalize():  # type: ignore
        while sessions:
            await sessions.pop().close()

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
    def go(routes):
        app = web.Application()

        for method, path, content, status in tuple(routes):

            async def handler(_):
                text = "" if not content else json.dumps(content)
                return web.Response(
                    text=text, content_type="application/json", status=status,
                )

            app.router.add_route(method, path, handler)

        return app

    yield go


@pytest.fixture
def mock_connection(mock_app, aiosnow_session):
    async def go(routes):
        server = mock_app(routes)
        return await aiosnow_session(server, server_kwargs={"skip_url_asserts": True})

    yield go


@pytest.fixture
def mock_table_model(mock_connection):
    async def go(model_cls, routes):
        _, client, _ = await mock_connection(
            routes or ["GET", "/api/now/table/test", None, 0]
        )
        return model_cls(client, table_name="test")

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
