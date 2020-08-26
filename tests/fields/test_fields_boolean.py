import pytest

from aiosnow.models.common.schema import BaseSchema, fields
from aiosnow.exceptions import DeserializationError


async def test_fields_boolean_type(mock_model):
    class TestSchema(BaseSchema):
        f_bool1 = fields.Boolean()

    schema = TestSchema()
    assert isinstance(schema.f_bool1, fields.Boolean)


async def test_fields_boolean_deserialize_plain_valid(mock_model):
    class TestSchema(BaseSchema):
        f_bool1 = fields.Boolean()
        f_bool2 = fields.Boolean()
        f_bool3 = fields.Boolean()
        f_bool4 = fields.Boolean()

    schema = TestSchema()
    data = schema.load({
        "f_bool1": True,
        "f_bool2": 1,
        "f_bool3": False,
        "f_bool4": 0
    })

    assert data["f_bool1"] is True
    assert data["f_bool2"] is True
    assert data["f_bool3"] is False
    assert data["f_bool4"] is False


async def test_fields_boolean_deserialize_plain_invalid(mock_model):
    class TestSchema(BaseSchema):
        f_bool1 = fields.Boolean()

    schema = TestSchema()

    with pytest.raises(DeserializationError):
        schema.load({"f_bool1": 2})
