from urllib.parse import urlparse

from snow.request import GetRequest


async def test_core_get_success(mock_resource):
    resp_content, resp_status = dict(result={"test_key": "test_value"}), 200

    resource = await mock_resource("GET", "/", resp_content, resp_status)
    response = await GetRequest(resource).send(url="/", transform=False)

    assert response.data == resp_content["result"]
    assert response.status == resp_status


async def test_core_get_path(mock_resource):
    resource = await mock_resource("GET", "/")
    request = GetRequest(resource)

    assert urlparse(request.url).path == urlparse(resource.url).path


async def test_core_get_params_query(mock_resource):
    query = "k1=v1^k2=v2"
    request = GetRequest(await mock_resource("GET"), query=query)
    assert request.params["sysparm_query"] == query


async def test_core_get_params_limit(mock_resource):
    limit = 15
    request = GetRequest(await mock_resource("GET"), limit)
    assert request.params["sysparm_limit"] == limit


async def test_core_params_offset(mock_resource):
    offset = 20
    request = GetRequest(await mock_resource("GET"), offset=offset)
    assert request.params["sysparm_offset"] == offset


async def test_core_get_params_page(mock_resource):
    limit = 15
    offset = 10

    request = GetRequest(await mock_resource("GET"), limit, offset)
    assert request.params["sysparm_limit"] == limit
    assert request.params["sysparm_offset"] == offset
