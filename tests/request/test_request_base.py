import pytest

from aiosnow.exceptions import RequestError, ServerError, UnexpectedResponseContent
from aiosnow.request import GetRequest


async def test_core_unexpected_response_content(mock_session):
    """Non-JSON data in content should raise an UnexpectedResponseContent"""

    session = await mock_session(server_path="/test")
    request = GetRequest("/test", session)

    with pytest.raises(UnexpectedResponseContent):
        await request.send()


async def test_core_error_full(mock_session, mock_error):
    """HTTP error response with null detail should work"""

    resp_content, resp_status = mock_error("test-message", 400, "test-detail")
    session = await mock_session(
        server_method="GET",
        server_path="/test",
        content=resp_content,
        status=resp_status,
    )
    request = GetRequest("/test", session)

    with pytest.raises(RequestError) as exc_info:
        await request.send()

    assert exc_info.value.message == "{message}: {detail}".format(
        **resp_content["error"]
    )
    assert exc_info.value.status == resp_status


async def test_core_error_message_only(mock_session, mock_error):
    """HTTP error response with null detail should work"""

    resp_content, resp_status = mock_error("test", 400)
    session = await mock_session(
        server_method="GET",
        server_path="/test",
        content=resp_content,
        status=resp_status,
    )
    request = GetRequest("/test", session)

    with pytest.raises(RequestError) as exc_info:
        await request.send()

    assert exc_info.value.message == resp_content["error"]["message"]
    assert exc_info.value.status == resp_status


async def test_core_error_fallback_500(mock_session):
    """Invalid content in response should be ignored, and the HTTP status message returned instead"""

    resp_content, resp_status = "invalid-content", 500
    session = await mock_session(
        server_method="GET",
        server_path="/test",
        content=resp_content,
        status=resp_status,
    )
    request = GetRequest("/test", session)

    with pytest.raises(ServerError) as exc_info:
        await request.send()

    assert exc_info.value.message == "Internal Server Error"
    assert exc_info.value.status == 500


async def test_core_response_204(mock_session):
    resp_content, resp_status = dict(result={"dsa": "asdf"}), 204

    session = await mock_session(
        server_method="GET",
        server_path="/test",
        content=resp_content,
        status=resp_status,
    )
    response = await GetRequest("/test", session).send()

    assert response.data == {}
    assert response.status == 204


async def test_core_response_malformed(mock_session):
    resp_content, resp_status = dict(result=""), 200

    session = await mock_session(
        server_method="GET",
        server_path="/test",
        content=resp_content,
        status=resp_status,
    )
    response = await GetRequest("/test", session).send()

    assert response.data == resp_content["result"]
    assert response.status == resp_status
