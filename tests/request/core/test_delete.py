from urllib.parse import urlparse

import pytest

from snow.exceptions import RequestError
from snow.request import DeleteRequest


async def test_core_delete(mock_resource):
    object_id = "test"
    resp_content, resp_status = {}, 204

    resource = await mock_resource("DELETE", f"/{object_id}", resp_content, resp_status)
    request = DeleteRequest(resource, object_id)
    response, content = await request._send(url=f"/{object_id}")

    assert urlparse(request.url).path.endswith(object_id)
    assert content == resp_content
    assert response.status == resp_status


async def test_core_delete_error(mock_error, mock_resource):
    object_id = "test"
    resp_content, resp_status = mock_error(
        message="Record doesn't exist or ACL restricts the record retrieval",
        detail="No Record found",
        status=404,
    )

    resource = await mock_resource("DELETE", f"/{object_id}", resp_content, resp_status)
    request = DeleteRequest(resource, object_id)

    with pytest.raises(RequestError) as exc_info:
        await request._send(url=f"/{object_id}")

    assert exc_info.value.message == "{message}: {detail}".format(
        **resp_content["error"]
    )
    assert exc_info.value.status == resp_status
