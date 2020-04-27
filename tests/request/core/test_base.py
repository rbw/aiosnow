import pytest

from snow.exceptions import RequestError, ServerError
from snow.request import GetRequest


async def test_error_message_only(mock_resource):
    """HTTP error response with null detail should work"""

    response = (
        dict(error=dict(message="[short msg]", detail=None,), status="failure"),
        400,
    )

    resource = await mock_resource("GET", "/", *response)
    request = GetRequest(resource)

    with pytest.raises(RequestError) as exc_info:
        await request._send(url="/")

    assert exc_info.value.message == "[short msg]"
    assert exc_info.value.status == 400


async def test_error_fallback_500(mock_resource):
    """Invalid content in response should be ignored, and the HTTP status message returned instead"""

    response = "asdf", 500
    resource = await mock_resource("GET", "/", *response)
    request = GetRequest(resource)

    with pytest.raises(ServerError) as exc_info:
        await request._send(url="/")

    assert exc_info.value.message == "Internal Server Error"
    assert exc_info.value.status == 500


async def test_error_fallback_503(mock_resource):
    """Null content in response should be ignored, and the HTTP status message returned instead"""

    response = None, 503
    resource = await mock_resource("GET", "/", *response)
    request = GetRequest(resource)

    with pytest.raises(ServerError) as exc_info:
        await request._send(url="/")

    assert exc_info.value.message == "Service Unavailable"
    assert exc_info.value.status == 503
