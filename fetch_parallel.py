import asyncio

from urllib.parse import urljoin, urlencode

from collections import deque

import aiohttp
import ujson

from marshmallow import Schema, fields, EXCLUDE, post_load


class Record(Schema):
    number = fields.String()


class Session:
    chunk_size = 1000
    base_url = ""
    connection = None
    queue = deque()

    def __init__(self, path):
        self.url = urljoin(self.base_url, path)

    async def __aenter__(self):
        self.connection = aiohttp.ClientSession(
            auth=aiohttp.helpers.BasicAuth(),
        )

        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.connection.close()

    def get_paged(self, limit, offset):
        query = urlencode({"sysparm_limit": limit, "sysparm_offset": offset})
        return f"{self.url}?{query}"

    async def get_chunked(self, limit=5, offset=0, concurrency=5):
        """Reads chunks in parallel

        :return:
        """

        urls = [self.get_paged(limit=limit, offset=c * (offset + limit)) for c in range(concurrency)]

        for response in await asyncio.gather(*[self.connection.request("GET", url, ssl=False) for url in urls]):
            result = ujson.loads(await response.text()).get("result")
            if not result:
                return

            yield result

        yield self.get_chunked(limit, limit * concurrency, concurrency) <-- invalid


async def get_many():
    async with Session("/api/now/table/incident") as session:
        async for result in session.get_chunked():
            print(result)
            content = Record().load(
                data=result,
                many=True,
                unknown=EXCLUDE
            )

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_many())
