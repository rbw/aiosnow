import ujson

from snowstorm.schemas import SnowErrorText
from snowstorm.consts import CONTENT_TYPE_EXPECTED
from snowstorm.exceptions import UnexpectedContentType, ErrorResponse


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
        content_type = self.obj.headers["content-type"]
        if not content_type.startswith(CONTENT_TYPE_EXPECTED):
            raise UnexpectedContentType(
                f"Unexpected content-type in response: {content_type}"
                f", expected: {CONTENT_TYPE_EXPECTED}"
            )

        content = ujson.loads(await self.obj.text())

        if "error" in content:
            err = SnowErrorText().load(content["error"])
            text = f"{err['message']({err['detail']})}" if err["detail"] else err["message"]
            raise ErrorResponse(text)

        return content.get("result")
