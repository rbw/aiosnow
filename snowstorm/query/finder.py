from .stream import Stream


class Finder:
    def __init__(self, resource, query):
        self.query = query
        self.resource = resource
        self.schema = resource.schema

    async def all(self, limit=30, offset=0, chunk_size=8):
        stream = Stream(self.resource, limit, offset, chunk_size)
        while not stream.exhausted:
            async for content in stream.read():
                for item in self.schema.load(content, many=True):
                    yield item

                print("CHUNK!")
