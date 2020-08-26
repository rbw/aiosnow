import pytest

from aiosnow.models.common.schema import BaseSchema, fields
from aiosnow.exceptions import DeserializationError


async def test_fields_integer_types(mock_model):
    class TestSchema(BaseSchema):
        f_int1 = fields.Integer()
        f_int2 = fields.Integer()
        f_intmap1 = fields.IntegerMap()

    schema = TestSchema()
    assert isinstance(schema.f_int1, fields.Integer)
    assert isinstance(schema.f_int2, fields.Integer)
    assert isinstance(schema.f_intmap1, fields.IntegerMap)


async def test_fields_integer_deserialize_plain_valid(mock_model):
    class TestSchema(BaseSchema):
        f_int1 = fields.Integer()

    schema = TestSchema()
    data = schema.load({
        "f_int1": 123
    })

    assert data["f_int1"] == 123


async def test_fields_integer_deserialize_plain_invalid(mock_model):
    class TestSchema(BaseSchema):
        f_int1 = fields.Integer()

    schema = TestSchema()

    with pytest.raises(DeserializationError):
        schema.load({"f_int1": "asdf"})


async def test_fields_integer_deserialize_mapping(mock_model):
    class TestSchema(BaseSchema):
        test_int = fields.IntegerMap()

    schema = TestSchema()
    data = schema.load(
        {
            "test_int": (3, "3 - High")
        }
    )

    assert data["test_int"].key == 3
    assert data["test_int"].value == "3 - High"
