import marshmallow
import ujson

from urllib.parse import urljoin

from snowstorm.exceptions import PayloadValidationError

from .base import PatchRequest


class Updater:
    def __init__(self, resource, object_id):
        self.resource = resource
        self.schema = resource.schema_cls
        self.object_id = object_id

    async def write(self, data):
        if not isinstance(data, dict):
            raise PayloadValidationError(
                f"Expected payload as a {dict}, got: {type(data)}"
            )

        try:
            payload = self.schema(
                unknown=marshmallow.EXCLUDE
            ).load({k.name: v for k, v in data.items()})
        except marshmallow.exceptions.ValidationError as e:
            raise PayloadValidationError(e)

        request = PatchRequest(self.resource, self.object_id, ujson.dumps(payload))
        response = await request.send()
        content = await response.read()
        return self.schema(unknown=marshmallow.RAISE).load(content)
