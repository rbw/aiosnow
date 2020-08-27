import pytest

from aiosnow.exceptions import DeserializationError
from aiosnow.models.common.schema import BaseSchema, fields
from aiosnow.query.utils import select


def test_fields_boolean_type():
    class TestSchema(BaseSchema):
        test_bool = fields.Boolean()

    schema = TestSchema()
    assert isinstance(schema.test_bool, fields.Boolean)


def test_fields_boolean_deserialize_plain_valid():
    class TestSchema(BaseSchema):
        test_bool1 = fields.Boolean()
        test_bool2 = fields.Boolean()
        test_bool3 = fields.Boolean()
        test_bool4 = fields.Boolean()

    schema = TestSchema()
    data = schema.load({"test_bool1": True, "test_bool2": 1, "test_bool3": False, "test_bool4": 0})

    assert data["test_bool1"] is True
    assert data["test_bool2"] is True
    assert data["test_bool3"] is False
    assert data["test_bool4"] is False


def test_fields_boolean_deserialize_plain_invalid():
    class TestSchema(BaseSchema):
        test_bool = fields.Boolean()

    schema = TestSchema()

    with pytest.raises(DeserializationError):
        schema.load({"test_bool": 2})


def test_fields_boolean_select_falsy():
    class TestSchema(BaseSchema):
        test_bool = fields.Boolean()

    assert select(TestSchema.test_bool.is_falsy()).sysparms == "test_bool!=true"


def test_fields_boolean_select_true():
    class TestSchema(BaseSchema):
        test_bool = fields.Boolean()

    assert select(TestSchema.test_bool.is_true()).sysparms == "test_bool=true"
