import marshmallow
import ujson

from snowstorm.exceptions import PayloadValidationError

from .base import PatchRequest


class Updater:
    def __init__(self, resource):
        self.resource = resource
        self.schema = resource.schema_cls

    async def write(self, **kwargs):
        try:
            payload = self.schema(unknown=marshmallow.EXCLUDE).load(kwargs)
        except marshmallow.exceptions.ValidationError as e:
            raise PayloadValidationError(e)

        """request = PatchRequest(self.resource, ujson.dumps(payload))
        response = await request.send()
        content = await response.read()
        return self.schema(unknown=marshmallow.RAISE).load(content)"""
        return {}
