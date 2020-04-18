import marshmallow
import ujson

from snow.exceptions import PayloadValidationError

from ..core import PatchRequest
from .base import RequestHelper


class Updater(RequestHelper):
    @property
    def schema(self):
        return self.resource.schema_cls(unknown=marshmallow.EXCLUDE)

    async def patch(self, object_id, data):
        if not isinstance(data, dict):
            raise PayloadValidationError(
                f"Expected payload as a {dict}, got: {type(data)}"
            )

        try:
            payload = self.schema.dumps(data)
        except marshmallow.exceptions.ValidationError as e:
            raise PayloadValidationError(e)

        _, content = await PatchRequest(
            self.resource, object_id, payload
        ).send()
        return self.schema.load(content)
