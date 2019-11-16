import aiohttp
import asyncio

from marshmallow import Schema, fields, EXCLUDE


class Post(Schema):
    id = fields.Integer()


async def execute(session, *args, **kwargs):
    print("EXECUTING REQ!")
    await asyncio.sleep(1)

    return await session.request(*args, **kwargs)


async def _yield_many(urls):
    async with aiohttp.ClientSession() as session:
        responses = []
        for response in await asyncio.gather(*[execute(session, "GET", url, ssl=False) for url in urls]):
            print("LOADING RESPONSE!")
            responses.append(response)

        for data in [await response.content.read() for response in responses]:
            print("LOAD,, CONCAT")

        # return Post().loads(data, many=True, unknown=EXCLUDE)


async def fetch_many(streams_max=2):
    urls = [
        "https://jsonplaceholder.typicode.com/comments", "https://jsonplaceholder.typicode.com/comments",
    ]

    data = await _yield_many(urls)

    print("DONE!")

    print(data)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(fetch_many())
