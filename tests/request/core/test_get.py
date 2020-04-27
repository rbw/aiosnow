from snow.request import GetRequest


async def test_get_one(mock_resource):
    resp_content, resp_status = dict(result={"test_key": "test_value"}), 200

    resource = await mock_resource("GET", "/", resp_content, resp_status)
    response, content = await GetRequest(resource)._send(url="/")

    assert content == resp_content["result"]
    assert response.status == resp_status


async def test_get_response_invalid(mock_resource):
    resp_content, resp_status = dict(result=""), 200

    resource = await mock_resource("GET", "/", resp_content, resp_status)
    response, content = await GetRequest(resource)._send(url="/")

    assert content == resp_content["result"]
    assert response.status == resp_status


async def test_params_query(dummy_resource):
    query = {"k1": "v1", "k2": "v2"}
    request = GetRequest(dummy_resource, query=query)
    assert request.params["sysparm_query"] == query


async def test_params_limit(dummy_resource):
    limit = 15
    request = GetRequest(dummy_resource, limit)
    assert request.params["sysparm_limit"] == limit


async def test_params_offset(dummy_resource):
    offset = 20
    request = GetRequest(dummy_resource, offset=offset)
    assert request.params["sysparm_offset"] == offset


async def test_params_page(dummy_resource):
    limit = 15
    offset = 10

    request = GetRequest(dummy_resource, limit, offset)
    assert request.params["sysparm_limit"] == limit
    assert request.params["sysparm_offset"] == offset
