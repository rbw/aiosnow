import pytest

from aiosnow.models.common.schema import BaseSchema, fields
from aiosnow.exceptions import DeserializationError


async def test_fields_string_types(mock_model):
    class TestSchema(BaseSchema):
        f_str1 = fields.String()
        f_str2 = fields.String()
        f_strmap1 = fields.StringMap()

    schema = TestSchema()
    assert isinstance(schema.f_str1, fields.String)
    assert isinstance(schema.f_str2, fields.String)
    assert isinstance(schema.f_strmap1, fields.StringMap)


async def test_fields_string_deserialize_plain_valid(mock_model):
    class TestSchema(BaseSchema):
        f_str1 = fields.String()

    schema = TestSchema()
    data = schema.load({
        "f_str1": "test123"
    })

    assert data["f_str1"] == "test123"


async def test_fields_string_deserialize_plain_invalid(mock_model):
    class TestSchema(BaseSchema):
        f_str1 = fields.String()

    schema = TestSchema()

    with pytest.raises(DeserializationError):
        schema.loads('{"f_str1": 1}')


async def test_fields_string_deserialize_mapping(mock_model):
    class TestSchema(BaseSchema):
        test_str = fields.StringMap()

    schema = TestSchema()
    data = schema.load(
        {
            "test_str": ("a83820b58f723300e7e16c7827bdedd2", "Hello"),
        }
    )

    assert data["test_str"].key == "a83820b58f723300e7e16c7827bdedd2"
    assert data["test_str"].value == "Hello"
