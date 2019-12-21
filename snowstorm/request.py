from abc import ABC, abstractmethod
from urllib.parse import urlencode

from snowstorm.response import Response


class Request(ABC):
    def __init__(self, resource):
        self._connection = resource.connection
        self._resource_url = resource.get_url()
        self._resource = resource

    @property
    @abstractmethod
    def _url(self):
        pass

    async def get(self, **kwargs):
        obj = await self._connection.get(self._url, **kwargs)
        return Response(obj)


class GetRequest(Request):
    def __init__(self, resource, limit=30, offset=0):
        super(GetRequest, self).__init__(resource)
        self._limit = limit
        self._offset = offset

    @property
    def _page_size(self):
        if not self._limit:
            return False

        return self._limit - self._offset

    @property
    def _url(self):
        params = dict(
            sysparm_offset=self._offset,
        )

        if self._page_size:
            params["sysparm_limit"] = self._page_size

        return f"{self._resource_url}&{urlencode(params)}"

