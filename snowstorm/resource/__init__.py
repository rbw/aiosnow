import re

from urllib.parse import urljoin, urlencode
from typing import Iterable
import aiohttp

from snowstorm.exceptions import (
    SnowstormException,
    NoSchemaFields,
    UnexpectedSchema,
    TooManyResults,
    NoResult,
    SchemaError,
    SelectError
)

from snowstorm.consts import Joined
from snowstorm.request import Reader, Creator, Updater

from .schema import Schema
from .query import QueryBuilder, Segment, select

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
        self.primary_key = self._get_primary_key()
        self.url = urljoin(self.config["address"], str(schema_cls.__location__))
        self._resolve = any([f for f in self.fields.values() if f.joined != Joined.VALUE])

    async def __aenter__(self):
        config = self.config
        self.connection = aiohttp.ClientSession(
            auth=aiohttp.helpers.BasicAuth(config["username"], config["password"]),
        )

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.connection.close()

    def _get_primary_key(self):
        primary_keys = [n for n, f in self.fields.items() if f.is_primary is True]

        if len(primary_keys) > 1:
            raise SchemaError(
                f"Multiple primary keys (is_primary) provided "
                f"for {self.name}. Maximum allowed is 1."
            )
        elif len(primary_keys) == 0:
            return None

        return primary_keys[0]

    @property
    def fields(self):
        schema_fields = getattr(self.schema_cls, "_declared_fields")
        if not schema_fields:
            raise NoSchemaFields(f"Schema {self.schema_cls} lacks fields definitions")

        return schema_fields

    @property
    def name(self):
        return self.schema_cls.__name__

    def get_url(self, fragments=None):
        if fragments and not isinstance(fragments, list):
            raise SnowstormException(f"Expected a list of path fragments, got: {fragments}")

        params = dict(
            sysparm_fields=",".join(self.fields),
            sysparm_display_value="all" if self._resolve else "false"
        )

        url = self.url

        if fragments:
            url += "/" + "/".join(fragments)

        return f"{url}{'?' + urlencode(params) if params else ''}"

    def get_reader(self, selection) -> Reader:
        builder = select(selection)
        return Reader(self, builder)

    def stream(self, selection, *args, **kwargs) -> Iterable:
        return self.get_reader(selection).stream(*args, **kwargs)

    async def get(self, selection, *args, **kwargs) -> dict:
        return await self.get_reader(selection).collect(*args, **kwargs)

    async def get_one(self, value):
        if not isinstance(value, Segment):
            raise SelectError(f"Expected a {self.name} field query, got {value}")

        if not self.primary_key:
            raise SchemaError(
                f'The selected resource "{self.name}" cannot '
                f'be queried: this schema lacks a field with "is_primary" set'
            )

        items = await self.get(QueryBuilder.from_segments([value]), limit=2)
        if len(items) > 1:
            raise TooManyResults("Too many results: expected one, got at least 2")
        elif len(items) == 0:
            raise NoResult("Expected a single object in response, got none")

        return items[0]

    async def get_object_id(self, value):
        record = await self.get_one(value)
        return record[self.primary_key]

    async def update(self, selection, payload) -> dict:
        if isinstance(selection, str):
            object_id = selection
        elif isinstance(selection, Segment):
            object_id = await self.get_object_id(selection)
        else:
            raise SelectError(f"Selection must be of type {Segment} or {str}")

        return await Updater(self, object_id).write(payload)

    async def create(self, payload) -> Creator:
        return await Creator(self).write(payload)
