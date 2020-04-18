import json
from marshmallow import Schema, fields

from snow.exceptions import ErrorResponse


class ErrorSchema(Schema):
    message = fields.String()
    detail = fields.String(allow_none=True)


_schema = ErrorSchema()


def load_content(data):
    content = json.loads(data)

    if "error" in content:
        err = _schema.load(content["error"])
        text = (
            f"{err['message']}: {err['detail']}"
            if err["detail"]
            else err["message"]
        )
        raise ErrorResponse(text)

    return content["result"]
