import re

from urllib.parse import urljoin, urlencode

import aiohttp

from snowstorm.exceptions import NoSchemaFields, UnexpectedSchema, SelectError
from snowstorm.consts import Target
from snowstorm.request import Reader, Creator, Updater

from .schema import Schema
from .query import QueryBuilder, Segment

from . import fields


class Resource:
    connection = None

    def __init__(self, schema_cls, config):
        self.config = config

        if not issubclass(schema_cls, Schema):
            raise UnexpectedSchema(f"Invalid schema class: {schema_cls}, must be of type {Schema}")
        if not re.match(r"^/.*", str(schema_cls.__location__)):
            raise UnexpectedSchema(
                f"Unexpected path in {schema_cls.__name__}.__location__: {schema_cls.__location__}"
            )

        self.schema_cls = schema_cls
        self.url = urljoin(self.config["address"], str(schema_cls.__location__))
        self._resolve = any([f for f in self.fields.values() if f.target != Target.VALUE])

    async def __aenter__(self):
        config = self.config
        self.connection = aiohttp.ClientSession(
            auth=aiohttp.helpers.BasicAuth(config["username"], config["password"]),
        )

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.connection.close()

    @property
    def fields(self):
        schema_fields = getattr(self.schema_cls, "_declared_fields")
        if not schema_fields:
            raise NoSchemaFields(f"Schema {self.schema_cls} lacks fields definitions")

        return schema_fields

    @property
    def name(self):
        return self.__class__.__name__

    def get_url(self, method="GET"):
        params = {}

        if method == "GET":
            params["sysparm_fields"] = ",".join(self.fields)
            params["sysparm_display_value"] = "all" if self._resolve else "false"

        return f"{self.url}{'?' + urlencode(params) if params else ''}"

    def get_builder(self, value):
        if isinstance(value, QueryBuilder):
            return value
        if isinstance(value, Segment):
            return QueryBuilder.from_segments(value.instances)
        elif isinstance(value, str):
            return QueryBuilder.from_raw(value)
        else:
            raise SelectError(f"Can only query by type {Segment} or {str}")

    def select(self, root):
        return self.get_builder(root)

    def stream(self, selection, *args, **kwargs):
        builder = self.get_builder(selection)
        return Reader(self, builder).stream(*args, **kwargs)

    def get(self, selection, *args, **kwargs):
        builder = self.get_builder(selection)
        return Reader(self, builder).collect(*args, **kwargs)

    async def update(self, payload, selection=None, sys_id=None) -> Updater:
        return await Updater(self).write(**payload)

    async def create(self, data) -> Creator:
        return await Creator(self).write(data)
