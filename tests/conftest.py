import json

import pytest
from aiohttp import web

from aiosnow import Client, fields
from aiosnow.models import BaseTableModel
from aiosnow.request.response import Response


class TestModel(BaseTableModel):
    @property
    def _api_url(self):
        return f"{self._client.base_url}/{self._table_name}"


TEST_TCP_ADDRESS = "127.0.0.1"


@pytest.fixture
def mock_error():
    def go(message, status, detail=None):
        return (
            dict(error=dict(message=message, detail=detail,), status="failure"),
            status,
        )

    yield go


@pytest.fixture
def mock_server():
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
def mock_client(aiohttp_client, mock_server):
    async def go(server_method="GET", server_path="/api/now/table/test", content="", status=0):
        server = mock_server(server_method, server_path, content, status)
        return await aiohttp_client(
            server, server_kwargs={"skip_url_asserts": True}, response_class=Response
        )

    yield go


@pytest.fixture
def mock_table_model(mock_server, mock_client):
    async def go(model_cls=TestModel, **kwargs):
        client = await mock_client(**kwargs)
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
