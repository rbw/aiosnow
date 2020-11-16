async def test_core_get_success(mock_table_model):
    resp_content, resp_status = dict(result={"test_key": "test_value"}), 200
    model = await mock_table_model(
        server_method="GET",
        content=resp_content,
        status=resp_status,
    )

    await model.get()

    # response = await GetRequest(api_url="/test", session=session).send()

    #assert response.data == resp_content["result"]
    #assert response.status == resp_status
