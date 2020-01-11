import marshmallow
import ujson

from ..core import DeleteRequest


class Deleter:
    def __init__(self, resource):
        self.resource = resource

    async def delete(self, object_id):
        request = DeleteRequest(self.resource, object_id)
        print(request.url)
        response = await request.send()
        content = await response.read()
        return content

    async def replace(self, data):
        pass
