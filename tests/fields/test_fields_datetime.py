import pytest

from aiosnow.models.common.schema import BaseSchema, fields
from aiosnow.exceptions import DeserializationError


async def test_fields_datetime_type(mock_model):
    class TestSchema(BaseSchema):
        f_dt1 = fields.DateTime()

    schema = TestSchema()
    assert isinstance(schema.f_dt1, fields.DateTime)


async def test_fields_datetime_deserialize_plain_valid(mock_model):
    class TestSchema(BaseSchema):
        f_dt1 = fields.DateTime()
        f_dt2 = fields.DateTime()

    schema = TestSchema()
    data = schema.load({
        "f_dt1": "2020-08-26 21:01:07",
        "f_dt2": "2020-08-26T21:01:07+00:00"
    })

    assert data["f_dt1"].year == data["f_dt2"].year == 2020
    assert data["f_dt1"].month == data["f_dt2"].month == 8
    assert data["f_dt1"].day == data["f_dt2"].day == 26
    assert data["f_dt1"].hour == data["f_dt2"].hour == 21
    assert data["f_dt1"].minute == data["f_dt2"].minute == 1
    assert data["f_dt1"].second == data["f_dt2"].second == 7


async def test_fields_datetime_deserialize_plain_invalid(mock_model):
    class TestSchema(BaseSchema):
        f_dt1 = fields.DateTime()

    schema = TestSchema()

    with pytest.raises(DeserializationError):
        schema.load({"f_dt1": "1234-12-56 50:20:30"})
