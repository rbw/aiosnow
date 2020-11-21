import pytest

from aiosnow.exceptions import ErrorResponse, RequestError, PayloadValidationError
from aiosnow.models import TableModel, fields


async def test_model_table_get(mock_table_model):
    class TestModel(TableModel):
        get_str = fields.String()
        get_int = fields.Integer()
        get_bool = fields.Boolean()
        get_dt = fields.DateTime()

    content = dict(
        result=dict(
            get_str="test", get_int=123, get_bool=True, get_dt="2020-01-01 01:00:00"
        )
    )

    model = await mock_table_model(
        TestModel, routes=[("GET", "/api/now/table/test", content, 200)],
    )

    response = await model.get()
    deserialized = response.data

    assert deserialized["get_str"] == "test"
    assert deserialized["get_int"] == 123
    assert deserialized["get_bool"] is True
    assert deserialized["get_dt"].year == 2020

    assert response.status == 200


async def test_model_table_get_503(mock_table_model):
    model = await mock_table_model(
        TableModel, routes=[("GET", "/api/now/table/test", None, 503)],
    )

    with pytest.raises(ErrorResponse) as excinfo:
        await model.get()

    assert excinfo.value.message == "Service Unavailable"
    assert excinfo.value.status == 503


async def test_model_table_get_404(mock_table_model):
    content = {
        "error": {
            "detail": "Record doesn't exist or ACL restricts the record retrieval",
            "message": "No Record found",
        },
        "status": "failure",
    }

    model = await mock_table_model(
        TableModel, routes=[("GET", "/api/now/table/test", content, 404)],
    )

    with pytest.raises(RequestError) as excinfo:
        await model.get()

    assert excinfo.value.message == "{message}: {detail}".format(**content["error"])
    assert excinfo.value.status == 404


async def test_model_table_create(mock_table_model):
    class TestModel(TableModel):
        test = fields.DateTime()

    content = dict(result=dict(test="2036-01-01T00:29:15+0000",))

    model = await mock_table_model(
        TestModel, routes=[("POST", "/api/now/table/test", content, 201)],
    )

    response = await model.create(payload=content["result"])

    assert response.data["test"].second == 15
    assert response.status == 201


async def test_model_table_create_400(mock_table_model):
    content = {
        "error": {"detail": None, "message": "Invalid table name"},
        "status": "failure",
    }

    model = await mock_table_model(
        TableModel, routes=[("POST", "/api/now/table/test", content, 400)]
    )

    with pytest.raises(RequestError) as excinfo:
        await model.create(payload={})

    assert excinfo.value.message == "Invalid table name"
    assert excinfo.value.status == 400


async def test_model_table_update(mock_table_model):
    class TestModel(TableModel):
        id = fields.Integer(is_primary=True)
        dt = fields.DateTime()

    object_id = "test123"
    content = {"result": {"id": 1, "dt": "2020-01-01 10:15:12",}}

    model = await mock_table_model(
        TestModel, routes=[("PATCH", f"/api/now/table/test/{object_id}", content, 201),],
    )

    response = await model.update(object_id, payload=content)

    assert response.data["dt"].minute == 15
    assert response.status == 201


async def test_model_table_update_invalid_payload(mock_table_model):
    class TestModel(TableModel):
        id = fields.Integer(is_primary=True)
        dt = fields.DateTime()

    object_id = "test123"

    model = await mock_table_model(
        TestModel, routes=[("PATCH", f"/api/now/table/test/{object_id}", None, 201),],
    )

    with pytest.raises(PayloadValidationError):
        await model.update(object_id, payload=[])

    with pytest.raises(PayloadValidationError):
        await model.update(object_id, payload=None)

    with pytest.raises(PayloadValidationError):
        await model.update(object_id, payload="test")
