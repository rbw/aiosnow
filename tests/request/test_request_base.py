import pytest

from aiosnow.exceptions import ErrorResponse, RequestError, UnexpectedResponseContent
from aiosnow.request import GetRequest


async def test_request_unexpected_response_content(mock_connection):
    """Non-JSON data in content should raise an UnexpectedResponseContent"""

    server, client, session = await mock_connection(
        [("GET", "/api/now/table/test", "", 200)]
    )
    request = GetRequest("/api/now/table/test", session)

    with pytest.raises(UnexpectedResponseContent):
        await request.send()


async def test_request_error_full(mock_connection, mock_error):
    """HTTP error response with null detail should work"""

    content, status = mock_error("test-message", 400, "test-detail")
    server, client, session = await mock_connection(
        [("GET", "/api/now/table/test", content, status)]
    )
    request = GetRequest("/api/now/table/test", session)

    with pytest.raises(RequestError) as exc_info:
        await request.send()

    assert exc_info.value.message == "{message}: {detail}".format(**content["error"])
    assert exc_info.value.status == status


async def test_request_error_message_only(mock_connection, mock_error):
    """HTTP error response with null detail should work"""

    content, status = mock_error("test", 400)
    server, client, session = await mock_connection(
        [("GET", "/api/now/table/test", content, status)]
    )
    request = GetRequest("/api/now/table/test", session)

    with pytest.raises(RequestError) as exc_info:
        await request.send()

    assert exc_info.value.message == content["error"]["message"]
    assert exc_info.value.status == status


async def test_request_error_fallback_500(mock_connection):
    """Invalid content in response should be ignored, and the HTTP status message returned instead"""

    content = "invalid-content"
    status = 500

    server, client, session = await mock_connection(
        [("GET", "/api/now/table/test", content, status)]
    )
    request = GetRequest("/api/now/table/test", session)

    with pytest.raises(ErrorResponse) as exc_info:
        await request.send()

    assert exc_info.value.message == "Internal Server Error"
    assert exc_info.value.status == 500


async def test_request_response_204(mock_connection):
    content = dict(result={"dsa": "asdf"})
    status = 204

    server, client, session = await mock_connection(
        [("GET", "/api/now/table/test", content, status)]
    )
    response = await GetRequest("/api/now/table/test", session).send()

    assert response.data == {}
    assert response.status == 204


async def test_request_response_malformed(mock_connection):
    content = dict(result="")
    status = 200

    server, client, session = await mock_connection(
        [("GET", "/api/now/table/test", content, status)]
    )
    response = await GetRequest("/api/now/table/test", session).send()

    assert response.data == content["result"]
    assert response.status == status
