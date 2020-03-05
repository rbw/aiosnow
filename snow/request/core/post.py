from .base import Request


class PostRequest(Request):
    __verb__ = "POST"

    def __init__(self, resource, payload):
        super(PostRequest, self).__init__(resource)
        self.payload = payload

    async def send(self, **kwargs):
        return await self._send(data=self.payload, **kwargs)

    @property
    def url(self):
        return self._resource_url
