from urllib.parse import urlparse

from aiosnow.request import DeleteRequest


async def test_core_delete_success(mock_client):
    object_id = "some_id"
    resp_content, resp_status = {}, 204

    session = await mock_client(
        server_method="DELETE",
        server_path=f"/test/{object_id}",
        content=resp_content,
        status=resp_status,
    )
    response = await DeleteRequest(
        api_url="/test", session=session, object_id=object_id
    ).send()

    assert not response.data
    assert response.status == resp_status


async def test_core_delete_path(mock_client):
    object_id = "some_id"
    session = await mock_client(
        server_method="DELETE", server_path=f"/test/{object_id}"
    )
    request = DeleteRequest(api_url="/test", session=session, object_id=object_id)

    assert urlparse(request.url).path.endswith(object_id)
