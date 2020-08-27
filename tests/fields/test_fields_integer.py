import pytest

from aiosnow.exceptions import DeserializationError
from aiosnow.models.common.schema import BaseSchema, fields
from aiosnow.query.utils import select


def test_fields_integer_types():
    class TestSchema(BaseSchema):
        test_int1 = fields.Integer()
        test_int2 = fields.Integer()
        test_intmap = fields.IntegerMap()

    schema = TestSchema()
    assert isinstance(schema.test_int1, fields.Integer)
    assert isinstance(schema.test_int2, fields.Integer)
    assert isinstance(schema.test_intmap, fields.IntegerMap)


def test_fields_integer_deserialize_plain_valid():
    class TestSchema(BaseSchema):
        test_int = fields.Integer()

    schema = TestSchema()
    data = schema.load({"test_int": 123})

    assert data["test_int"] == 123


def test_fields_integer_deserialize_plain_invalid():
    class TestSchema(BaseSchema):
        test_int = fields.Integer()

    schema = TestSchema()

    with pytest.raises(DeserializationError):
        schema.load({"test_int": "asdf"})


def test_fields_integer_deserialize_mapping():
    class TestSchema(BaseSchema):
        test_int = fields.IntegerMap()

    schema = TestSchema()
    data = schema.load({"test_int": (3, "3 - High")})

    assert data["test_int"].key == 3
    assert data["test_int"].value == "3 - High"


def test_fields_integer_query_between():
    class TestSchema(BaseSchema):
        test_int = fields.Integer()

    assert select(TestSchema.test_int.between(1, 3)).sysparms == "test_intBETWEEN1@3"


def test_fields_integer_query_equals():
    class TestSchema(BaseSchema):
        test_int = fields.Integer()

    assert select(TestSchema.test_int.equals(0)).sysparms == "test_int=0"


def test_fields_integer_greater_or_equals():
    class TestSchema(BaseSchema):
        test_int = fields.Integer()

    assert select(TestSchema.test_int.greater_or_equals(0)).sysparms == "test_int>=0"


def test_fields_integer_greater_than():
    class TestSchema(BaseSchema):
        test_int = fields.Integer()

    assert select(TestSchema.test_int.greater_than(2)).sysparms == "test_int>2"


def test_fields_integer_less_or_equals():
    class TestSchema(BaseSchema):
        test_int = fields.Integer()

    assert select(TestSchema.test_int.less_or_equals(2)).sysparms == "test_int<=2"


def test_fields_integer_less_than():
    class TestSchema(BaseSchema):
        test_int = fields.Integer()

    assert select(TestSchema.test_int.less_than(2)).sysparms == "test_int<2"


def test_fields_integer_not_equals():
    class TestSchema(BaseSchema):
        test_int = fields.Integer()

    assert select(TestSchema.test_int.not_equals(2)).sysparms == "test_int!=2"
