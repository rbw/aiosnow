import pytest

from aiosnow.exceptions import DeserializationError
from aiosnow.models.common.schema import BaseSchema, fields
from aiosnow.query.utils import select


def test_fields_string_types():
    class TestSchema(BaseSchema):
        test_str1 = fields.String()
        test_str2 = fields.String()
        test_strmap = fields.StringMap()

    schema = TestSchema()
    assert isinstance(schema.test_str1, fields.String)
    assert isinstance(schema.test_str2, fields.String)
    assert isinstance(schema.test_strmap, fields.StringMap)


def test_fields_string_deserialize_plain_valid():
    class TestSchema(BaseSchema):
        test_str = fields.String()

    schema = TestSchema()
    data = schema.load({"test_str": "test123"})

    assert data["test_str"] == "test123"


def test_fields_string_deserialize_plain_invalid():
    class TestSchema(BaseSchema):
        test_str = fields.String()

    schema = TestSchema()

    with pytest.raises(DeserializationError):
        schema.load({"test_str": 1})


def test_fields_string_deserialize_mapping():
    class TestSchema(BaseSchema):
        test_str = fields.StringMap()

    schema = TestSchema()
    data = schema.load({"test_str": ("a83820b58f723300e7e16c7827bdedd2", "Hello"),})

    assert data["test_str"].key == "a83820b58f723300e7e16c7827bdedd2"
    assert data["test_str"].value == "Hello"


def test_fields_string_query_between():
    class TestSchema(BaseSchema):
        test_str = fields.String()

    assert (
        select(TestSchema.test_str.between("q", "t")).sysparms == "test_strBETWEENq@t"
    )


def test_fields_string_query_ends_with():
    class TestSchema(BaseSchema):
        test_str = fields.String()

    assert (
        select(TestSchema.test_str.ends_with("outage")).sysparms
        == "test_strENDSWITHoutage"
    )


def test_fields_string_query_equals():
    class TestSchema(BaseSchema):
        test_str = fields.String()

    assert select(TestSchema.test_str == "test").sysparms == "test_str=test"
    assert select(TestSchema.test_str.equals("test")).sysparms == "test_str=test"


def test_fields_string_query_greater_or_equals():
    class TestSchema(BaseSchema):
        test_str = fields.String()

    assert select(TestSchema.test_str.greater_or_equals("s")).sysparms == "test_str>=s"


def test_fields_string_query_less_or_equals():
    class TestSchema(BaseSchema):
        test_str = fields.String()

    assert select(TestSchema.test_str.less_or_equals("s")).sysparms == "test_str<=s"


def test_fields_string_query_not_contains():
    class TestSchema(BaseSchema):
        test_str = fields.String()

    assert select(TestSchema.test_str.not_contains("SAP")).sysparms == "test_str!*SAP"


def test_fields_string_query_not_equals():
    class TestSchema(BaseSchema):
        test_str = fields.String()

    assert (
        select(
            TestSchema.test_str.not_equals("Network storage is unavailable")
        ).sysparms
        == "test_str!=Network storage is unavailable"
    )
