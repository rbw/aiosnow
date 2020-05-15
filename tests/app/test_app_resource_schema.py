import pytest

from snow.exceptions import NoSchemaLocation, UnexpectedSchema
from snow.resource import Schema, fields


def test_schema_missing_location(mock_app_raw):
    """Schema missing Meta.location should raise NoSchemaLocation"""

    class TestSchema(Schema):
        test = fields.Text()

    app = mock_app_raw
    with pytest.raises(NoSchemaLocation):
        app.resource(TestSchema)


def test_schema_invalid_type(mock_app_raw):
    """Schema of unknown type should raise UnexpectedSchema"""

    class TestSchema:
        test = fields.Text()

    app = mock_app_raw
    with pytest.raises(UnexpectedSchema):
        app.resource(TestSchema)


def test_schema_valid_location(mock_app_raw):
    """Schema with a valid location should work"""

    class TestSchema(Schema):
        class Meta:
            location = "/test"

        test = fields.Text()

    app = mock_app_raw
    resource = app.resource(TestSchema)
    assert resource.schema.snow_meta.location == "/test"


def test_schema_invalid_location(mock_app_raw):
    """Schema with an invalid location should fail"""

    class TestSchema(Schema):
        class Meta:
            location = "test"

        test = fields.Text()

    app = mock_app_raw

    with pytest.raises(UnexpectedSchema):
        app.resource(TestSchema)
