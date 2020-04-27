import json

import pytest
from aiohttp import web

from snow import Application
from snow.resource import Resource, Schema, fields


class DefaultSchema(Schema):
    __location__ = "/test"

    test = fields.Text()


@pytest.fixture
def mock_error():
    def go(message, status, detail=None):
        return (
            dict(error=dict(message=message, detail=detail,), status="failure"),
            status,
        )

    yield go


@pytest.fixture
def mock_client(aiohttp_client):
    async def go(mock_server):
        return await aiohttp_client(
            mock_server, server_kwargs={"skip_url_asserts": True}
        )

    yield go


@pytest.fixture
def mock_app(mock_client):
    async def go(connect_to):
        app = Application(
            config_data=dict(
                address="test.service-now.com",
                basic_auth=("test", "test"),
                use_ssl=False,
            )
        )
        get_session = await mock_client(connect_to)
        app.get_session = lambda: get_session
        return app

    yield go


@pytest.fixture
async def dummy_resource(mock_resource):
    return await mock_resource("GET", "/", None, None)


@pytest.fixture
def mock_resource(mock_server_app, mock_resource_raw):
    async def go(method, path, *response):
        server = mock_server_app(method, path, *response)
        return await mock_resource_raw(connect_to=server)

    yield go


@pytest.fixture
def mock_resource_raw(mock_app):
    async def go(connect_to):
        return Resource(DefaultSchema, await mock_app(connect_to))

    yield go


@pytest.fixture
def mock_server_app():
    def go(method, path, content, status):
        async def handler(_):
            return web.Response(
                text=json.dumps(content), content_type="application/json", status=status
            )

        app = web.Application()
        app.router.add_route(method, path, handler)
        return app

    yield go
