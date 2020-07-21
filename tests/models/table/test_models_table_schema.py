import pytest

from aiosnow.exceptions import UnexpectedModelSchema
from aiosnow.model import fields
from aiosnow.models.table import TableModel, TableSchema


async def test_models_table_schema_meta_valid(mock_model):
    """Schema with a valid table_name should work"""

    class TestSchema(TableSchema):
        class Meta:
            table_name = "test"

        test = fields.String()

    await mock_model(model=TableModel, schema=TestSchema)


async def test_models_table_schema_invalid_type(mock_model):
    """Schema of unknown type should raise UnexpectedSchema"""

    class TestSchema:
        test = fields.String()

    with pytest.raises(UnexpectedModelSchema):
        await mock_model(model=TableModel, schema=TestSchema)


async def test_models_table_schema_meta_invalid(mock_model):
    """Schema with an invalid Meta should fail"""

    class TestSchema(TableSchema):
        class Meta:
            pass

        test = fields.String()

    with pytest.raises(NotImplementedError):
        await mock_model(model=TableModel, schema=TestSchema)
