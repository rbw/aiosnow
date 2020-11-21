import json
from urllib.parse import urlparse

from aiosnow.request import PostRequest


async def test_request_post_success(mock_connection):
    content = dict(result={"test_key": "test_value"})
    status = 201

    server, client, session = await mock_connection(
        [("POST", "/api/now/table/test", content, status)]
    )
    response = await PostRequest(
        "/api/now/table/test", session, payload=json.dumps(content)
    ).send()

    assert response.data == content["result"]
    assert response.status == status


async def test_request_post_path(mock_connection):
    server, client, session = await mock_connection(
        [("POST", "/api/now/table/test", None, 201)]
    )
    request = PostRequest("/api/now/table/test", session, payload="")

    assert urlparse(request.url).path == "/api/now/table/test"
