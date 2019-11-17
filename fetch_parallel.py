import asyncio

from queue import SimpleQueue
from urllib.parse import urljoin, urlencode

import aiohttp
import ujson

from marshmallow import Schema, fields, EXCLUDE, post_load


class Record(Schema):
    number = fields.String()


class ExecutionQueue:
    def __init__(self, session, size, count):
        self._position = 0
        self._session = session
        self.is_depleted = False
        self.count = count
        self.size = size
        # super(ExecutionQueue, self).__init__()

    @property
    def connection(self):
        return self._session.connection

    @property
    def url(self):
        return self._session.url

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position = value

    @property
    def targets(self):
        for c in range(self.count):
            query = urlencode({"sysparm_limit": self.size, "sysparm_offset": c * (self.size + self._position)})
            yield f"{self.url}?{query}"

    async def execute(self):
        responses = await asyncio.gather(
            *[self.connection.request("GET", url, ssl=False) for url in self.targets]
        )

        for response in responses:
            content = ujson.loads(await response.text()).get("result")
            if not content:
                self.is_depleted = True
                return

            yield response.status, content

        self.position = self.count * (self.size + self._position)


class Session:
    chunk_size = 1000
    base_url = ""
    connection = None

    def __init__(self, path):
        self.url = urljoin(self.base_url, path)

    async def __aenter__(self):
        self.connection = aiohttp.ClientSession(
            auth=aiohttp.helpers.BasicAuth(),
        )

        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.connection.close()

    async def get_chunked(self, limit=5, offset=0, concurrency=5):
        """Reads chunks in parallel"""

        queue = ExecutionQueue(session=self, size=50, count=5)
        while not queue.is_depleted:
            async for status, content in queue.execute():
                yield status

            # yield ujson.loads(await response.text()).get("result")

        """def get_targets():
            return [self._get_pages(limit=limit, offset=offset + limit) for c in range(concurrency)]

        while len(self.queue):
            for response in await asyncio.gather(*[self.connection.request("GET", url, ssl=False) for url in urls]):
                if not result:
                    return

                yield result"""


async def get_many():
    async with Session("/api/now/table/incident") as session:
        async for result in session.get_chunked():
            print(result)
            pass

            """print(result)
            content = Record().load(
                data=result,
                many=True,
                unknown=EXCLUDE
            )

            print(content)"""

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_many())
