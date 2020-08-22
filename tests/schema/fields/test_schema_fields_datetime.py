from aiosnow.models.common.schema import BaseSchema, fields


async def test_schema_fields_datetime(mock_model):
    class TestSchema(BaseSchema):
        f_dt1 = fields.DateTime()

    print(TestSchema.f_dt1)
