import aiohttp
import asyncio

from marshmallow import Schema, fields, EXCLUDE


class Post(Schema):
    id = fields.Integer()


async def execute(method, **kwargs):
    async with aiohttp.ClientSession() as session:
        response = await session.request(method, "https://jsonplaceholder.typicode.com/comments", **kwargs)
        content = await response.content.read()
        print(content)
        # yield Post().loads(obj, unknown=EXCLUDE)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(execute(method="GET"))
