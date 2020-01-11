import marshmallow
import ujson

from ..core import DeleteRequest


class Deleter:
    def __init__(self, resource):
        self.resource = resource

    async def delete(self, object_id):
        request = DeleteRequest(self.resource, object_id)
        response = await request.send()
        return await response.read()

    async def replace(self, data):
        pass
