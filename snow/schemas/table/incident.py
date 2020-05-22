from snow.model import fields
from snow.models.table import TableSchema


class IncidentSchema(TableSchema):
    class Meta:
        table_name = "incident"

    sys_id = fields.Text(is_primary=True)
    number = fields.Text()
    description = fields.Text()
    short_description = fields.Text()
    impact = fields.Numeric()
    opened_at = fields.Datetime()
