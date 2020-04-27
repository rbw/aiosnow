from __future__ import annotations

from typing import TYPE_CHECKING

import marshmallow

from snow.exceptions import PayloadValidationError

from ..core import PostRequest
from .base import RequestHelper

if TYPE_CHECKING:
    from snow.resource import Schema


class Creator(RequestHelper):
    @property
    def schema(self) -> Schema:
        return self.resource.schema_cls(unknown=marshmallow.RAISE)

    async def write(self, data: dict) -> dict:
        try:
            payload = self.schema.dumps(data)
        except marshmallow.exceptions.ValidationError as e:
            raise PayloadValidationError(e)

        _, content = await PostRequest(self.resource, payload).send()
        return self.schema.load(content)
