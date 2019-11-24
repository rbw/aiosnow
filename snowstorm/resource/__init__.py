import aiohttp

from urllib.parse import urljoin
from marshmallow import fields

from snowstorm.query import Finder

from .schema import Schema, SchemaOpts


class Resource:
    connection = None

    def __init__(self, schema_cls, config):
        self.config = config
        self.schema = schema_cls()
        self.fields = self.schema.declared_fields.keys()
        self.url = urljoin(config["base_url"], schema_cls.__location__)

    async def __aenter__(self):
        config = self.config
        self.connection = aiohttp.ClientSession(
            auth=aiohttp.helpers.BasicAuth(config["username"], config["password"]),
        )

        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.connection.close()

    def find(self, query):
        return Finder(self, query)
