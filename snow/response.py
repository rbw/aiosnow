import ujson

from marshmallow import Schema, fields

from snow.exceptions import UnexpectedContentType, ErrorResponse
from snow.consts import CONTENT_TYPE


class ErrorSchema(Schema):
    message = fields.String()
    detail = fields.String(allow_none=True)


class Response:
    def __init__(self, obj):
        self.obj = obj

    @property
    def status(self):
        return self.obj.status

    @property
    def links(self):
        return self.obj.links

    async def read(self):
        if self.obj.method == "DELETE":
            return dict(result="success")

        content_type = self.obj.headers.get("content-type", None)

        if not content_type.startswith(CONTENT_TYPE):
            raise UnexpectedContentType(
                f"Unexpected content-type in response: "
                f"{content_type}, expected: {CONTENT_TYPE}, "
                f"probable causes: instance down or REST API disabled"
            )

        content = ujson.loads(await self.obj.text())

        if "error" in content:
            err = ErrorSchema().load(content["error"])
            text = f"{err['message']} ({self.status}): {err['detail']}" if err["detail"] else err["message"]
            raise ErrorResponse(text)

        return content.get("result")
