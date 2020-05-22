import json

import pytest
from aiohttp import web

from snow.app import Snow
from snow.config import ConfigSchema
from snow.model.base import BaseModel, BaseSchema, fields
from snow.request.response import Response
from snow.utils import get_url


class TestSchema(BaseSchema):
    test = fields.Text()


class TestModel(BaseModel):
    pass


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
def mock_session(aiohttp_client, mock_server):
    async def go(server_method="GET", server_path="/", content="", status=0):
        server = mock_server(server_method, server_path, content, status)
        return await aiohttp_client(
            server, server_kwargs={"skip_url_asserts": True}, response_class=Response,
        )

    yield go


@pytest.fixture
def mock_app():
    return Snow(
        address="test.service-now.com", basic_auth=("test", "test"), use_ssl=False
    )


@pytest.fixture
def mock_model(mock_session, mock_model_raw):
    async def go(
        server_method="GET",
        server_path="/",
        content=None,
        status=0,
        model=TestModel,
        schema=TestSchema,
    ):
        session = await mock_session(
            server_method, server_path, content or dict(result=""), status
        )
        return await mock_model_raw(session, server_path, model, schema)

    yield go


@pytest.fixture
def mock_model_raw():
    async def go(session, path, model, schema):
        config = ConfigSchema(many=False).load(dict(address=TEST_TCP_ADDRESS))
        url = get_url(address=config.address, use_ssl=False)
        return model(
            schema_cls=schema, instance_url=url + path, session=session, config=config,
        )

    yield go
