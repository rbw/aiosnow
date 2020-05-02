import json
from urllib.parse import urlparse

from snow.request import PostRequest


async def test_core_post_success(mock_resource):
    resp_content, resp_status = dict(result={"test_key": "test_value"}), 201

    resource = await mock_resource("POST", "/", resp_content, resp_status)
    response, content = await PostRequest(resource, json.dumps(resp_content))._send(
        url="/"
    )

    assert content == resp_content["result"]
    assert response.status == resp_status


async def test_core_post_path(mock_resource):
    resource = await mock_resource("POST", "/")
    request = PostRequest(resource, "")

    assert urlparse(request.url).path == urlparse(resource.url).path
