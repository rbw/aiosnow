from marshmallow import Schema, fields


class ErrorSchema(Schema):
    """Defines the structure of the ServiceNow error response content"""

    message = fields.String()
    detail = fields.String(allow_none=True)


class ContentSchema(Schema):
    """Defines structure of the ServiceNow response content"""

    error = fields.Nested(ErrorSchema)
    result = fields.Raw()
    status = fields.String(missing=None)
