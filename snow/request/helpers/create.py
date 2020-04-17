import marshmallow
import ujson

from snow.exceptions import PayloadValidationError

from ..core import PostRequest
from .base import RequestHelper


class Creator(RequestHelper):
    @property
    def schema(self):
        return self.resource.schema_cls(unknown=marshmallow.RAISE)

    async def write(self, data):
        try:
            payload = self.schema.load(data)
        except marshmallow.exceptions.ValidationError as e:
            raise PayloadValidationError(e)

        _, content = await PostRequest(self.resource, ujson.dumps(payload)).send()
        return self.schema.load(content)
