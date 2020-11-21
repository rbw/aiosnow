from urllib.parse import urlparse

from aiosnow.request import DeleteRequest


async def test_request_delete_success(mock_connection):
    object_id = "some_id"
    status = 204

    server, client, session = await mock_connection(
        [("DELETE", f"/api/now/table/test/{object_id}", None, status)]
    )
    response = await DeleteRequest(
        "/api/now/table/test", session, object_id=object_id
    ).send()

    assert not response.data
    assert response.status == status


async def test_request_delete_path(mock_connection):
    object_id = "some_id"
    server, client, session = await mock_connection(
        [("DELETE", f"/api/now/table/test/{object_id}", None, 204)]
    )
    request = DeleteRequest("/api/now/table/test", session, object_id=object_id)

    assert urlparse(request.url).path.endswith(object_id)
