from abc import ABC, abstractmethod

from aiohttp import ClientSession
from snow.response import Response
from snow.consts import CONTENT_TYPE


class Request(ABC):
    _session: ClientSession

    def __init__(self, resource):
        self._session = resource.session
        self._resource_url = resource.get_url()
        self._resource = resource
        self.default_headers = {
            "Content-type": CONTENT_TYPE
        }

    @property
    @abstractmethod
    def url(self):
        pass

    @abstractmethod
    async def send(self):
        pass

    @property
    @abstractmethod
    def __verb__(self):
        pass

    async def _request(self, **kwargs):
        headers = self.default_headers
        headers.update(kwargs.pop("headers", {}))

        obj = await self._session.request(
            self.__verb__,
            self.url,
            headers={
                **self.default_headers,
                **(headers or {})
            },
            **kwargs
        )

        return Response(obj)
