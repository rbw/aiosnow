from typing import Iterable

from snowstorm.consts import SORT_ASCENDING, SORT_DESCENDING

from .stream import PageStream


class Reader:
    def __init__(self, resource, query):
        self.resource = resource
        self.query = query
        self.schema = resource.schema_cls()

    def _order_by(self, value, ascending=True):
        items = value if isinstance(value, list) else [value]
        sort = SORT_ASCENDING if ascending else SORT_DESCENDING

        prefix = "^" if self.query else ""
        return prefix + "^".join([f"{sort}{item.name}" for item in items])

    def order_desc(self, value):
        self.query += self._order_by(value, ascending=False)
        return self

    def order_asc(self, value):
        self.query += self._order_by(value)
        return self

    async def stream(self, *args, **kwargs) -> Iterable:
        stream = PageStream(self.resource, *args, **kwargs, query=self.query)
        while not stream.exhausted:
            async for content in stream.read():
                for item in self.schema.load(content, many=True):
                    yield item

    def get_one(self):
        raise NotImplementedError
