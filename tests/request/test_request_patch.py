import json
from urllib.parse import urlparse

from aiosnow.request import PatchRequest


async def test_core_patch_success(mock_session):
    object_id = "some_id"
    resp_content, resp_status = dict(result={"test_key": "updated value"}), 200

    session = await mock_session(
        server_method="PATCH",
        server_path=f"/test/{object_id}",
        content=resp_content,
        status=resp_status,
    )
    response = await PatchRequest(
        api_url="/test",
        session=session,
        object_id=object_id,
        payload=json.dumps(resp_content),
    ).send()

    assert response.data == resp_content["result"]
    assert response.status == resp_status


async def test_core_patch_path(mock_session):
    object_id = "some_id"
    resp_content, resp_status = dict(result={"test_key": "updated value"}), 200

    session = await mock_session(
        server_method="PATCH",
        server_path=f"/test/{object_id}",
        content=resp_content,
        status=resp_status,
    )
    request = PatchRequest(
        api_url="/test",
        session=session,
        object_id=object_id,
        payload=json.dumps(resp_content),
    )

    assert urlparse(request.url).path.endswith(object_id)
