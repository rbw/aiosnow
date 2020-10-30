import pytest

from aiosnow.exceptions import SchemaError
from aiosnow.models import ModelSchema, Pluck, fields
from aiosnow.query.fields import IntegerQueryable, StringQueryable


def to_mapping(key, value):
    return dict(value=key, display_value=value)


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


def test_model_schema_dumps_loads():
    class MainDocument(ModelSchema):
        test1 = fields.String()
        test2 = fields.Integer()

    dict_obj = dict(test1="test", test2=123)

    json_obj = MainDocument().dumps(dict_obj)
    assert isinstance(json_obj, str)

    loaded = MainDocument().loads(json_obj)
    assert loaded == dict_obj


def test_model_schema_loads():
    class MainDocument(ModelSchema):
        test1 = fields.String()
        test2 = fields.Integer()

    json_obj = """{"test1": "test", "test2": 123}"""
    dict_obj = dict(test1="test", test2=123)

    assert MainDocument().loads(json_obj) == dict_obj


def test_model_schema_nested():
    class RelatedDocument(ModelSchema):
        test2 = fields.String()
        test3 = fields.Integer(pluck=Pluck.VALUE)

    class MainDocument(ModelSchema):
        test1 = fields.String(pluck=Pluck.DISPLAY_VALUE)
        related = RelatedDocument

    json_obj = """
    {
        "test1": {"value": "test", "display_value": "test2"},
        "related":
        {
            "test2": {"value": "test1", "display_value": "test2"},
            "test3": {"value": 123, "display_value": "test2"}
        }
    }
    """

    dict_obj = dict(test1="test2", related=dict(test2="test1", test3=123))

    query = MainDocument.related.test2.equals("test123")
    assert str(query) == "related.test2=test123"

    main = MainDocument()
    assert main.loads(json_obj) == dict_obj

    related = main.nested_fields["related"].schema
    assert isinstance(related, RelatedDocument)
    assert set(related.fields.keys()) == {"test2", "test3"}
