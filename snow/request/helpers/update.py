import marshmallow
import ujson

from snow.exceptions import PayloadValidationError

from ..core import PatchRequest


class Updater:
    def __init__(self, resource):
        self.resource = resource
        self.schema = resource.schema_cls

    async def patch(self, object_id, data):
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

        response = await PatchRequest(self.resource, object_id, ujson.dumps(payload)).send()
        content = await response.read()
        return self.schema(unknown=marshmallow.RAISE).load(content)

    async def replace(self, data):
        pass
