from aiosnow.models.common.schema import BaseSchema, fields


async def test_schema_fields_email(mock_model):
    class TestSchema(BaseSchema):
        f_email1 = fields.Email()

    print(TestSchema.f_email1)
