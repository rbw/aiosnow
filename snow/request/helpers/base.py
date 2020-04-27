from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from snow.resource import Resource, Schema


class RequestHelper:
    def __init__(self, resource: Resource):
        self.resource = resource
        self.session = resource.session

    @property
    def schema(self) -> Schema:
        raise NotImplementedError
