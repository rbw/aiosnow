from .stream import Stream


class Finder:
    def __init__(self, resource, query):
        self.query = query
        self.resource = resource
        self.schema = resource.schema

    async def all(self, limit=None, offset=None):
        stream = Stream(self.resource, limit, offset)
        async for content in stream.read():
            for item in self.schema.load(content, many=True):
                yield item
