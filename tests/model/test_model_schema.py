import pytest

from aiosnow.exceptions import SchemaError
from aiosnow.models import ModelSchema, fields
from aiosnow.query.fields import IntegerQueryable, StringQueryable


def test_model_schema_field_registration():
    class TestSchema(ModelSchema):
        test1 = fields.String()
        test2 = fields.Integer()

    assert isinstance(TestSchema.test1, StringQueryable)
    assert isinstance(TestSchema.test2, IntegerQueryable)
    assert isinstance(TestSchema.fields["test1"], fields.String)
    assert isinstance(TestSchema.fields["test2"], fields.Integer)


def test_model_schema_primary_key():
    with pytest.raises(SchemaError):
        type(
            "TestSchema",
            (ModelSchema,),
            dict(
                test1=fields.String(is_primary=True),
                test2=fields.Integer(is_primary=True),
            ),
        )


def test_model_schema_nested():
    pass


def test_model_schema_dumps():
    pass


def test_model_schema_loads():
    pass


def test_model_schema_load_response_content():
    pass


def test_model_schema_dump_request_payload():
    pass
