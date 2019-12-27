from abc import ABC, abstractmethod

from aiohttp import ClientSession
from snowstorm.response import Response
from snowstorm.consts import CONTENT_TYPE


class Request(ABC):
    _connection: ClientSession

    def __init__(self, resource):
        self._connection = resource.connection
        self._resource_url = resource.get_url()
        self._resource = resource
        self.default_headers = {
            "Content-type": "application/json"
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
    def __http_method__(self):
        pass

    async def _request(self, **kwargs):
        headers = self.default_headers

        obj = await self._connection.request(
            self.__http_method__,
            self.url,
            headers=self.default_headers,
            **kwargs
        )

        return Response(obj)
