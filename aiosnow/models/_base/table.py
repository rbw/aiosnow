import json
from abc import abstractmethod
from typing import Any, AsyncGenerator, Union

from aiosnow.client import Client
from aiosnow.exceptions import (
    DeleteError,
    NoItems,
    PayloadValidationError,
    RequestError,
    SchemaError,
    SelectError,
    TooManyItems,
    UnexpectedResponseContent,
)
from aiosnow.query import Condition, Selector, select
from aiosnow.request import Pagestream, Response, methods

from .._base.model import BaseModel


class BaseTableModel(BaseModel):
    """Abstract table model"""

    def __init__(
        self, client: Client, table_name: str = None, return_only: list = None,
    ):
        self._table_name = table_name
        self._return_only = return_only
        super(BaseTableModel, self).__init__(client)

    @property
    @abstractmethod
    def _api_url(self) -> Any:
        pass

    async def stream(
        self, selection: Union[Selector, Condition, str] = None, **kwargs: Any
    ) -> AsyncGenerator:
        """Stream-like async generator

        Chunk size determines the number of records to fetch in one go.
        Setting a lower chunk size decreases memory usage, but increases the
        number of requests sent to the server.

        Keyword Args:
            selection: aiosnow-compatible query
            limit (int): Maximum number of records to return
            offset (int): Starting record index
            page_size (int): Number of records to fetch in one go

        Yields:
            Chunk of records
        """

        stream = Pagestream(
            api_url=self._api_url,
            query=select(selection).sysparms,
            session=self._session,
            fields=kwargs.pop("return_only", self._return_only)
            or self.schema.fields.keys(),
            nested_fields=self._nested_fields,
            **kwargs,
        )

        while not stream.exhausted:
            async for response in stream.get_next():
                for record in self.schema.load_content(response.data, many=True):
                    yield response, record

    async def get(
        self, selection: Union[Selector, Condition, str] = None, **kwargs: Any
    ) -> Response:
        """Buffered many

        Fetch and store the entire result in memory.

        Note: It's recommended to use the stream method when dealing with a
        large number of records.

        Keyword Args:
            selection: Aiosnow-compatible query
            limit (int): Maximum number of records to return
            offset (int): Starting record index

        Returns:
            Response
        """

        return await self.request(
            methods.GET,
            query=select(selection).sysparms,
            nested_fields=self._nested_fields,
            resolve=True,
            **kwargs,
        )

    async def get_one(
        self, selection: Union[Selector, Condition, str] = None, **kwargs: Any
    ) -> Response:
        """Get one record

        Args:
            selection: aiosnow-compatible query

        Returns:
            Response
        """

        if not self._primary_key:
            raise SchemaError(
                f'The targeted "{self.__class__}" cannot be queried: '
                f'its schema lacks a field with "is_primary" set'
            )

        response = await self.get(selection, limit=2, **kwargs)
        if not isinstance(response.data, list):
            raise UnexpectedResponseContent(
                f"Expected a {list} in response to get_one(), got: {type(response.data)}",
                status=response.status,
            )
        elif len(response) > 1:
            raise TooManyItems("Too many results: expected one, got at least 2")
        elif len(response) < 1:
            raise NoItems("Expected a single object in response, got none")

        # Assign the matched record
        response.data = response.data[0]

        return response

    async def get_object_id(self, value: Union[Selector, Condition, str]) -> str:
        """Get object id by str or Condition

        Immediately return if value is of str type.

        Args:
            value: Condition or str

        Returns:
            Object id
        """

        if isinstance(value, Condition):
            response = await self.get_one(value, return_only=[self._primary_key])
            return response[self._primary_key]
        elif isinstance(value, str):
            return value
        else:
            raise SelectError(
                f"Selection must be of type {Condition} or {str}, not {type(value)}"
            )

    async def update(self, selection: Union[Condition, str], payload: dict) -> Response:
        """Update matching record

        Args:
            selection: Condition or ID of object to update
            payload: Update payload

        Returns:
            Response
        """

        sys_id = await self.get_object_id(selection)

        if not isinstance(payload, dict):
            raise PayloadValidationError(
                f"Expected payload as a {dict}, got: {type(payload)}"
            )

        return await self.request(
            methods.PATCH, object_id=sys_id, payload=json.dumps(payload),
        )

    async def create(self, payload: dict) -> Response:
        """Create a new record

        Args:
            payload: New record payload

        Returns:
            Response
        """

        return await self.request(methods.POST, payload=json.dumps(payload),)

    async def delete(self, selection: Union[Condition, str]) -> Response:
        """Delete matching record

        Args:
            selection: Condition or ID

        Returns:
            Response
        """

        try:
            sys_id = await self.get_object_id(selection)
        except NoItems:
            raise DeleteError("Cannot delete, no such record")

        response = await self.request(methods.DELETE, object_id=sys_id, decode=False)

        if response.status != 204:
            text = await response.text()
            raise RequestError(
                f"Unexpected response for DELETE request. "
                f"Status: {response.status}, Text: {text}",
                response.status,
            )

        return response
