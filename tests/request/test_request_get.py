from aiosnow.request import GetRequest


async def test_request_get_success(mock_connection):
    content = dict(result={"test_key": "test_value"})
    status = 200
    server, client, session = await mock_connection(
        [("GET", "/api/now/table/test", content, status)]
    )
    response = await GetRequest("/api/now/table/test", session).send()

    assert response.data == content["result"]
    assert response.status == status


async def test_request_get_params_query(mock_connection):
    query = "k1=v1^k2=v2"
    server, client, session = await mock_connection(
        [("GET", "/api/now/table/test", None, 200)]
    )
    request = GetRequest("/api/now/table/test", session, query=query)
    assert request.params["sysparm_query"] == query


async def test_request_get_params_limit(mock_connection):
    limit = 15
    server, client, session = await mock_connection(
        [("GET", "/api/now/table/test", None, 200)]
    )
    request = GetRequest("/api/now/table/test", session, limit=limit)
    assert request.params["sysparm_limit"] == limit


async def test_request_params_offset(mock_connection):
    offset = 20
    server, client, session = await mock_connection(
        [("GET", "/api/now/table/test", None, 200)]
    )
    request = GetRequest("/api/now/table/test", session, offset=offset)
    assert request.params["sysparm_offset"] == offset


async def test_request_get_params_page(mock_connection):
    limit = 15
    offset = 10
    server, client, session = await mock_connection(
        [("GET", "/api/now/table/test", None, 200)]
    )
    request = GetRequest("/api/now/table/test", session, limit=limit, offset=offset)
    assert request.params["sysparm_limit"] == limit + offset
    assert request.params["sysparm_offset"] == offset
