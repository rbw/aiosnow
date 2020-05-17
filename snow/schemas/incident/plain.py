from snow.resource import Schema, fields


class IncidentPlain(Schema):
    class Meta:
        location = "/api/now/table/incident"

    sys_id = fields.Text(is_primary=True)
    number = fields.Text()
    description = fields.Text()
    short_description = fields.Text()
    impact = fields.Numeric()
    opened_at = fields.Datetime()
