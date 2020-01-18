from .base import Request


class DeleteRequest(Request):
    __verb__ = "DELETE"

    def __init__(self, resource, object_id):
        super(DeleteRequest, self).__init__(resource)
        self._resource_url = resource.get_url(fragments=[object_id])

    async def send(self):
        return await self._request()

    @property
    def url(self):
        return self._resource_url
