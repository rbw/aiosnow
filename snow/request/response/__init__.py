from typing import Iterable, Union

from aiohttp import ClientResponse, client_exceptions, http_exceptions, web_exceptions
from marshmallow import EXCLUDE

from snow.exceptions import RequestError, ServerError, UnexpectedResponseContent

from .schemas import ContentSchema, ErrorSchema


class Response(ClientResponse):
    data: Union[list, dict]

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {hex(id(self))} {self.url.path} [{self.status} {self.reason}]>"

    def __getitem__(self, item):
        return self.data[item]

    def __iter__(self) -> Iterable:
        yield from self.data

    def __len__(self) -> int:
        return len(self.data)

    async def load(self) -> None:
        data = await self.json()

        if not isinstance(data, dict):
            if self.status == 204:
                self.data = {}
                return

            await self._handle_error()

        content = ContentSchema(unknown=EXCLUDE, many=False).load(data)
        if "error" in content:
            err = content["error"]
            msg = (
                f"{err['message']}: {err['detail']}"
                if err["detail"]
                else err["message"]
            )

            raise RequestError(msg, self.status)

        self.data = content["result"]

    async def _handle_error(self) -> None:
        try:
            # Something went wrong, most likely out of the ServiceNow application's control:
            # Raise exception if we got a HTTP error status back.
            self.raise_for_status()
        except (
            client_exceptions.ClientResponseError,
            http_exceptions.HttpProcessingError,
        ) as exc:
            raise ServerError(exc.message, exc.code) from exc
        except web_exceptions.HTTPException as exc:
            raise ServerError(exc.text or "", exc.status) from exc
        else:
            # Non-JSON content along with a HTTP 200 returned: Unexpected.
            text = await self.text()
            raise UnexpectedResponseContent(
                f"Unexpected response received from server: {text}", 200
            )
