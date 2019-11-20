import asyncio

from urllib.parse import urljoin, urlencode, parse_qs

import aiohttp
import ujson

from marshmallow import Schema, fields, EXCLUDE, post_load


class Record(Schema):
    number = fields.String()


class FetchQueue:
    def __init__(self, session, chunk_size, concurrency):
        self.chunk_size = chunk_size
        self.concurrency = concurrency
        self.is_depleted = False
        self._group_offset = 0
        self._session = session

    @property
    def connection(self):
        return self._session.connection

    @property
    def url(self):
        return self._session.url

    def _get_next_urls(self):
        for c in range(self.concurrency):
            query = urlencode({
                "sysparm_limit": self.chunk_size,
                "sysparm_offset": self._group_offset + self.chunk_size
            })

            yield f"{self.url}?{query}"

    async def consume_many(self, method="GET", **kwargs):
        targets = self._get_next_urls()
        responses = await asyncio.gather(*[self.connection.request(method, url, **kwargs) for url in targets])

        if "next" not in responses[-1].links:
            self.is_depleted = True
            return

        group_url_next = str(responses[-1].links["next"]["url"])
        self._group_offset = int(parse_qs(group_url_next).get("sysparm_offset")[0])

        for response in responses:
            yield ujson.loads(await response.text()).get("result")


class Session:
    base_url = "https://dev49212.service-now.com"
    connection = None

    def __init__(self, path):
        self.url = urljoin(self.base_url, path)

    async def fetch(self, chunk_size=20, concurrency=5):
        queue = FetchQueue(self, chunk_size, concurrency)
        while not queue.is_depleted:
            async for content in queue.consume_many():
                for item in Record().load(content, many=True, unknown=EXCLUDE):
                    yield item

    async def __aenter__(self):
        self.connection = aiohttp.ClientSession(
            auth=aiohttp.helpers.BasicAuth("admin", "Bajskorv123!"),
        )

        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.connection.close()


async def get_many():
    async with Session("/api/now/table/incident") as session:
        async for record in session.fetch():
            print(record)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_many())



