from urllib.parse import urlparse

from snow.request import DeleteRequest


async def test_core_delete_success(mock_resource):
    object_id = "test"
    resp_content, resp_status = {}, 204

    resource = await mock_resource("DELETE", f"/{object_id}", resp_content, resp_status)
    request = DeleteRequest(resource, object_id)
    response = await request.send(url=f"/{object_id}")

    assert not response.data
    assert response.status == resp_status


async def test_core_delete_path(mock_resource):
    object_id = "some_id"
    resource = await mock_resource("DELETE", f"/{object_id}")
    request = DeleteRequest(resource, object_id)

    assert urlparse(request.url).path.endswith(object_id)
