import marshmallow
import ujson

from snowstorm.exceptions import PayloadValidationError
from snowstorm.request.base import PostRequest


class Writer:
    def __init__(self, resource):
        self.resource = resource
        self.schema = resource.schema_cls

    def create(self, **kwargs):
        raise NotImplementedError


class AsyncWriter(Writer):
    async def create(self, **kwargs):
        try:
            payload = self.schema(unknown=marshmallow.RAISE).load(kwargs)
        except marshmallow.exceptions.ValidationError as e:
            raise PayloadValidationError(e)

        request = PostRequest(self.resource, ujson.dumps(payload))
        response = await request.send()
        return await response.read()


class SyncWriter(Writer):
    pass
