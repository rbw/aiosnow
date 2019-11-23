import aiohttp

from urllib.parse import urljoin
from marshmallow import fields

from snowstorm.query import Finder

from .schema import ResourceSchema, SchemaOpts


class Resource:
    base_url = ""
    connection = None

    def __init__(self, schema_cls):
        self.schema = schema_cls()
        self.url = urljoin(self.base_url, schema_cls.__location__)

    async def __aenter__(self):
        self.connection = aiohttp.ClientSession(
            auth=aiohttp.helpers.BasicAuth(),
        )

        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.connection.close()

    def find(self, query):
        return Finder(self, query)

