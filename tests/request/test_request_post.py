import json
from urllib.parse import urlparse

from aiosnow.request import PostRequest


async def test_core_post_success(mock_client):
    resp_content, resp_status = dict(result={"test_key": "test_value"}), 201

    session = await mock_client(
        server_method="POST",
        server_path="/test",
        content=resp_content,
        status=resp_status,
    )

    response = await PostRequest(
        "/test", session=session, payload=json.dumps(resp_content)
    ).send()

    assert response.data == resp_content["result"]
    assert response.status == resp_status


async def test_core_post_path(mock_client):
    session = await mock_client(server_method="POST", server_path="/test")
    request = PostRequest("/test", session=session, payload="")

    assert urlparse(request.url).path == "/test"
