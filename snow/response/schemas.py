from marshmallow import Schema, fields


class SnowErrorText(Schema):
    message = fields.String()
    detail = fields.String(allow_none=True)
