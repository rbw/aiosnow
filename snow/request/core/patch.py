from .base import Request


class PatchRequest(Request):
    __verb__ = "PATCH"

    def __init__(self, resource, object_id, payload):
        super(PatchRequest, self).__init__(resource)
        self.payload = payload
        self._resource_url = resource.get_url(fragments=[object_id])

    async def send(self):
        return await self._request(data=self.payload)

    @property
    def url(self):
        return self._resource_url
