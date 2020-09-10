from aiosnow.models import TableModel, fields


class JournalModel(TableModel):
    sys_id = fields.String(is_primary=True)
    sys_created_on = fields.DateTime()
    sys_created_by = fields.String()
    element = fields.String()
    element_id = fields.String()
    name = fields.String()
    value = fields.String()
    sys_tags = fields.String()
