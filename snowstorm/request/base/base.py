from abc import ABC, abstractmethod

from aiohttp import ClientSession
from snowstorm.response import Response


class Request(ABC):
    _connection: ClientSession

    def __init__(self, resource):
        self._connection = resource.connection
        self._resource_url = resource.get_url()
        self._resource = resource

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
        obj = await self._connection.request(self.__http_method__, self.url, **kwargs)
        return Response(obj)
