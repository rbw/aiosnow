import json
from urllib.parse import urlparse

from aiosnow.request import PatchRequest


async def test_request_patch_success(mock_connection):
    object_id = "some_id"
    content = dict(result={"test_key": "updated value"})
    status = 200

    server, client, session = await mock_connection(
        [("PATCH", f"/api/now/table/test/{object_id}", content, 200)]
    )
    response = await PatchRequest(
        "/api/now/table/test",
        session,
        object_id=object_id,
        payload=json.dumps(content),
    ).send()

    assert response.data == content["result"]
    assert response.status == status


async def test_request_patch_path(mock_connection):
    object_id = "some_id"
    content = dict(result={"test_key": "updated value"})

    server, client, session = await mock_connection(
        [("PATCH", f"/api/now/table/test/{object_id}", content, 200)]
    )
    request = PatchRequest(
        "/api/now/table/test",
        session,
        object_id=object_id,
        payload=json.dumps(content),
    )

    assert urlparse(request.url).path.endswith(object_id)
