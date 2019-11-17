import asyncio

from urllib.parse import urljoin, urlencode

import aiohttp
import ujson

from marshmallow import Schema, fields, EXCLUDE, post_load


class Record(Schema):
    number = fields.String()


class RequestGroup:
    def __init__(self, session, size, count):
        self._position = 0
        self._session = session
        self.is_depleted = False
        self.count = count
        self.size = size
        super(RequestGroup, self).__init__()

    @property
    def connection(self):
        return self._session.connection

    @property
    def queue(self):
        return self._session.queue

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
            query = urlencode({"sysparm_limit": self.size, "sysparm_offset": c * (self.size + self.position)})
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

            # yield response.status, content
            for item in content:
                yield item

        self.position = self.count * (self.size + self._position)


class Session:
    base_url = ""
    connection = None

    def __init__(self, path):
        self.url = urljoin(self.base_url, path)
        self.group = RequestGroup(session=self, size=10, count=5)

    async def __aenter__(self):
        self.connection = aiohttp.ClientSession(
            auth=aiohttp.helpers.BasicAuth(),
        )

        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.connection.close()

    async def pump(self):
        while not self.group.is_depleted:
            async for item in self.group.execute():
                yield item


async def get_many():
    async with Session("/api/now/table/incident") as session:
        async for result in session.pump():
            print(result["number"])

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_many())
