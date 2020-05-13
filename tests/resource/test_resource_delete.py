import pytest

from snow.exceptions import RequestError


async def test_core_delete_non_existent(mock_error, mock_resource):
    object_id = "test"
    resp_content, resp_status = mock_error(
        message="",
        status=404,
    )

    resource = await mock_resource("DELETE", f"/{object_id}", resp_content, resp_status)

    with pytest.raises(RequestError) as exc_info:
        await resource.delete(object_id)

    assert exc_info.value.status == resp_status
