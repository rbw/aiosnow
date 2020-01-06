from .base import Request


class PatchRequest(Request):
    __http_method__ = "POST"

    def __init__(self, resource, payload):
        super(PatchRequest, self).__init__(resource)
        self.payload = payload

    async def send(self):
        return await self._request(data=self.payload)

    @property
    def url(self):
        return self._resource_url
