import json
from urllib.parse import urlparse

from snow.request import PatchRequest


async def test_core_patch_success(mock_resource):
    object_id = "test123"
    resp_content, resp_status = dict(result={"test_key": "updated value"}), 200

    resource = await mock_resource("PATCH", "/", resp_content, resp_status)
    response = await PatchRequest(
        resource, object_id, json.dumps(resp_content)
    ).send(url="/", transform=False)

    assert response.data == resp_content["result"]
    assert response.status == resp_status


async def test_core_patch_path(mock_resource):
    object_id = "some_id"
    resource = await mock_resource("PATCH", f"/{object_id}")
    request = PatchRequest(resource, object_id, "")

    assert urlparse(request.url).path.endswith(object_id)
