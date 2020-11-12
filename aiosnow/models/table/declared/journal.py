from aiosnow.models import ModelSchema, TableModel, fields


class JournalModelSchema(ModelSchema):
    sys_id = fields.String(is_primary=True)
    sys_created_on = fields.DateTime()
    sys_created_by = fields.String()
    element = fields.String()
    element_id = fields.String()
    name = fields.String()
    value = fields.String()
    sys_tags = fields.String()


class JournalModel(TableModel):
    schema_cls = JournalModelSchema
