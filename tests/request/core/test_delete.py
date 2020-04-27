import pytest

from snow.exceptions import RequestError
from snow.request import DeleteRequest


async def test_delete_ok(mock_resource):
    object_id = 123

    response = None, 204
    resource = await mock_resource("DELETE", f"/{object_id}", *response)
    request = DeleteRequest(resource, object_id)
    response, content = await request._send(url=f"/{object_id}")

    assert content is None
    assert response.status == 204


async def test_delete_error(mock_resource):
    object_id = 123

    response = (
        dict(
            error=dict(
                message="Record doesn't exist or ACL restricts the record retrieval",
                detail="No Record found",
            ),
            status="failure",
        ),
        404,
    )

    resource = await mock_resource("DELETE", f"/{object_id}", *response)
    request = DeleteRequest(resource, object_id)

    with pytest.raises(RequestError) as exc_info:
        await request._send(url=f"/{object_id}")

    assert (
        exc_info.value.message
        == "Record doesn't exist or ACL restricts the record retrieval: No Record found"
    )
    assert exc_info.value.status == 404
