from typing import Any, Iterable, Union

from aiohttp import ClientResponse, client_exceptions, http_exceptions, web_exceptions
from marshmallow import EXCLUDE

from aiosnow.exceptions import (
    InvalidContentMethod,
    RequestError,
    ServerError,
    UnexpectedResponseContent,
)

from .schemas import ContentSchema


class Response(ClientResponse):
    """Aiosnow Response class

    The Response object holds information about the ServiceNow HTTP response.

    Subclass of aiohttp.ClientResponse, its base reference documentation can be found here:
    https://docs.aiohttp.org/en/latest/client_reference.html#aiohttp.ClientResponse

    Attributes:
        - data: Deserialized (ContentSchema) response content
        - status: HTTP status code of response (int), e.g. 200
        - reason: HTTP status reason of response (str), e.g. "OK"
        - url: Request URL
    """

    def __init__(self, *args: Any, **kwargs: Any):
        super(Response, self).__init__(*args, **kwargs)
        self.data: Union[list, dict, None] = None

    def __repr__(self) -> str:
        return (
            f"<{self.__class__.__name__} {hex(id(self))} {self.url.path} "
            f"[{self.status} {self.reason}]>"
        )

    def __getitem__(self, name: Any) -> Any:
        if isinstance(self.data, dict):
            return self.data.get(name)

        return None

    def __iter__(self) -> Iterable:
        if isinstance(self.data, list):
            yield from self.data
        elif isinstance(self.data, dict):
            yield from self.data.keys()
        else:
            raise InvalidContentMethod(f"Cannot iterate over type: {type(self.data)}")

    def __len__(self) -> int:
        if isinstance(self.data, list):
            return len(self.data)

        return 1

    async def load_document(self) -> None:
        """Deserialize and set response content

        Raises:
            RequestError: If there was an error in the request-response content
        """

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
        """Something went seriously wrong.

        This method interprets the error-response and raises the appropriate exception.

        Raises:
            - ServerError: If the error was interpreted as an unhandled server error
            - UnexpectedResponseContent: If the request was successful, but the request-response contains
            unexpected data
        """

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
