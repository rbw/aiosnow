from urllib.parse import urljoin, urlencode
from typing import Iterable, Type, Union

from snow.exceptions import (
    SnowException,
    NoSchemaFields,
    TooManyItems,
    NoItems,
    SchemaError,
    SelectError
)

from snow.consts import Joined
from snow.request import Reader, Creator, Updater, Deleter
from snow.config import ConfigSchema

from .schema import Schema
from .query import QueryBuilder, Condition, select

from . import fields


class Resource:
    """ServiceNow API Resource Model

    Args:
        schema_cls (Schema): Schema class
        app (Application): Application instance

    Attributes:
        config (ConfigSchema): Application config
        url: API URL
        fields: Schema fields
    """

    def __init__(self, schema_cls: Union[Type[Schema], Schema], app):
        self.app = app

        # Read Resource schema
        self.schema_cls = schema_cls
        self.fields = self._get_fields()
        self.primary_key = self._get_primary_key()

        # Configure self
        self.config = self.app.config
        self.url = urljoin(self.config.address, str(schema_cls.__location__))
        self._resolve = any([f for f in self.fields.values() if f.joined != Joined.VALUE])

        # Create helpers
        self.reader = Reader(self)
        self.updater = Updater(self)
        self.creator = Creator(self)
        self.deleter = Deleter(self)

    async def __aenter__(self):
        self.session = self.app.get_session()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    def _get_primary_key(self):
        primary_keys = [n for n, f in self.fields.items() if f.is_primary is True]

        if len(primary_keys) > 1:
            raise SchemaError(
                f"Multiple primary keys (is_primary) supplied "
                f"in {self.name}. Maximum allowed is 1."
            )
        elif len(primary_keys) == 0:
            return None

        return primary_keys[0]

    def _get_fields(self):
        schema_fields = getattr(self.schema_cls, "_declared_fields")
        if not schema_fields:
            raise NoSchemaFields(f"Schema {self.schema_cls} lacks fields definitions")

        return schema_fields

    @property
    def name(self):
        return self.schema_cls.__name__

    def get_url(self, fragments=None):
        if fragments and not isinstance(fragments, list):
            raise SnowException(f"Expected a list of path fragments, got: {fragments}")

        params = dict(
            sysparm_fields=",".join(self.fields),
            sysparm_display_value="all" if self._resolve else "false"
        )

        url = self.url

        if fragments:
            url += "/" + "/".join(fragments)

        return f"{url}{'?' + urlencode(params) if params else ''}"

    def stream(self, selection=None, **kwargs) -> Iterable:
        """Stream-like async generator

        Fetches data in chunks using the ServiceNow pagination system.

        Chunk size determines the number of records to fetch in one go, and can be
        tweaked to

        Keyword Args:
            selection: Snow compatible query
            limit (int): Maximum number of records to return
            offset (int): Starting record index
            chunk_size (int): Number of records to fetch in one go

        Yields:
            list: Chunk of records
        """

        return self.reader.stream(
            select(selection).sysparms,
            **kwargs
        )

    async def get(self, selection=None, **kwargs) -> dict:
        """Buffered many

        Fetches data and stores in buffer.

        Note: It's recommended to use the stream method when dealing with large
        number of records.

        Keyword Args:
            selection: Snow compatible query
            limit (int): Maximum number of records to return
            offset (int): Starting record index

        Returns:
            list: Records
        """

        return await self.reader.collect(
            select(selection).sysparms,
            **kwargs
        )

    async def get_one(self, selection=None):
        """Get one record

        Args:
            selection: Snow compatible query

        Returns:
            dict: Record
        """

        if not self.primary_key:
            raise SchemaError(
                f'The selected resource "{self.name}" cannot '
                f'be queried: this schema lacks a field with "is_primary" set'
            )

        items = await self.get(selection, limit=2)
        if len(items) > 1:
            raise TooManyItems("Too many results: expected one, got at least 2")
        elif len(items) == 0:
            raise NoItems("Expected a single object in response, got none")

        return items[0]

    async def get_pk_value(self, selection):
        """Given a selection, return the resulting record's PK field's value

        Args:
            selection: Snow compatible query

        Returns:
            str: PK field's value
        """

        record = await self.get_one(selection)
        return record[self.primary_key]

    async def get_object_id(self, value):
        """Get object id by str or Condition

        Immediately return if value is str.

        Args:
            value: Condition or str

        Returns:
            str: Object id
        """

        if isinstance(value, str):
            return value
        elif isinstance(value, Condition):
            return await self.get_pk_value(value)
        else:
            raise SelectError(f"Selection must be of type {Condition} or {str}")

    async def update(self, selection, payload) -> dict:
        """Update matching record

        Args:
            selection: Condition or ID
            payload (dict): Update payload

        Returns:
            dict: Updated record
        """

        object_id = await self.get_object_id(selection)
        return await self.updater.patch(object_id, payload)

    async def create(self, payload):
        """Create a new record

        Args:
            payload (dict): New record payload

        Returns:
            dict: Created record
        """

        return await self.creator.write(payload)

    async def delete(self, selection):
        """Delete matching record

        Args:
            selection: Condition or ID

        Returns:
            dict: {"result": <status>}
        """
        object_id = await self.get_object_id(selection)
        return await self.deleter.delete(object_id)
