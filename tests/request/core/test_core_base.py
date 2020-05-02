import pytest

from snow.exceptions import RequestError, ServerError, UnexpectedResponseContent
from snow.request import GetRequest


async def test_core_unexpected_response_content(mock_resource):
    """Non-JSON data in content should raise an UnexpectedResponseContent"""

    resp_content, resp_status = "non-json-data", 200
    resource = await mock_resource("GET", "/", resp_content, resp_status)
    request = GetRequest(resource)

    with pytest.raises(UnexpectedResponseContent):
        await request._send(url="/")


async def test_core_error_full(mock_resource, mock_error):
    """HTTP error response with null detail should work"""

    resp_content, resp_status = mock_error("test-message", 400, "test-detail")
    resource = await mock_resource("GET", "/", resp_content, resp_status)

    request = GetRequest(resource)

    with pytest.raises(RequestError) as exc_info:
        await request._send(url="/")

    assert exc_info.value.message == "{message}: {detail}".format(
        **resp_content["error"]
    )
    assert exc_info.value.status == resp_status


async def test_core_error_message_only(mock_resource, mock_error):
    """HTTP error response with null detail should work"""

    resp_content, resp_status = mock_error("test", 400)
    resource = await mock_resource("GET", "/", resp_content, resp_status)

    request = GetRequest(resource)

    with pytest.raises(RequestError) as exc_info:
        await request._send(url="/")

    assert exc_info.value.message == resp_content["error"]["message"]
    assert exc_info.value.status == resp_status


async def test_core_error_fallback_500(mock_resource):
    """Invalid content in response should be ignored, and the HTTP status message returned instead"""

    resp_content, resp_status = "invalid-content", 500
    resource = await mock_resource("GET", "/", resp_content, resp_status)
    request = GetRequest(resource)

    with pytest.raises(ServerError) as exc_info:
        await request._send(url="/")

    assert exc_info.value.message == "Internal Server Error"
    assert exc_info.value.status == 500


async def test_core_response_204(mock_resource):
    resp_content, resp_status = dict(result={"dsa": "asdf"}), 204

    resource = await mock_resource("GET", "/", resp_content, resp_status)
    response, content = await GetRequest(resource)._send(url="/")

    assert content == {}
    assert response.status == 204


async def test_core_response_malformed(mock_resource):
    resp_content, resp_status = dict(result=""), 200

    resource = await mock_resource("GET", "/", resp_content, resp_status)
    response, content = await GetRequest(resource)._send(url="/")

    assert content == resp_content["result"]
    assert response.status == resp_status
