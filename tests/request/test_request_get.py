from snow.request import GetRequest


async def test_core_get_success(mock_session):
    resp_content, resp_status = dict(result={"test_key": "test_value"}), 200
    session = await mock_session(
        server_method="GET",
        server_path="/test",
        content=resp_content,
        status=resp_status,
    )
    response = await GetRequest(api_url="/test", session=session).send()

    assert response.data == resp_content["result"]
    assert response.status == resp_status


async def test_core_get_params_query(mock_session):
    query = "k1=v1^k2=v2"
    session = await mock_session(server_method="GET", server_path="/test")
    request = GetRequest(api_url="/test", session=session, query=query)
    assert request.url_params["sysparm_query"] == query


async def test_core_get_params_limit(mock_session):
    limit = 15
    session = await mock_session(server_method="GET", server_path="/test")
    request = GetRequest(api_url="/test", session=session, limit=limit)
    assert request.url_params["sysparm_limit"] == limit


async def test_core_params_offset(mock_session):
    offset = 20
    session = await mock_session(server_method="GET", server_path="/test")
    request = GetRequest(api_url="/test", session=session, offset=offset)
    assert request.url_params["sysparm_offset"] == offset


async def test_core_get_params_page(mock_session):
    limit = 15
    offset = 10
    session = await mock_session(server_method="GET", server_path="/test")
    request = GetRequest(api_url="/test", session=session, limit=limit, offset=offset)
    assert request.url_params["sysparm_limit"] == limit + offset
    assert request.url_params["sysparm_offset"] == offset
