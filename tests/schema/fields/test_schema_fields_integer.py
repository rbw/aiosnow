from aiosnow.models.common.schema import BaseSchema, fields


async def test_schema_fields_integer(mock_model):
    class TestSchema(BaseSchema):
        f_int1 = fields.Integer()
        f_int2 = fields.Integer()
        f_intmap1 = fields.IntegerMap()
        f_intchoice1 = fields.IntegerChoice()

    print(TestSchema.f_int1)
