import asyncio

from snowstorm.resource import Schema, fields
from snowstorm import Snowstorm


class Incident(Schema):
    __location__ = "/api/now/table/incident"
    __resolve__ = True

    number = fields.String()
    sys_id = fields.String()


async def main():
    snow = Snowstorm(dict(

    ))

    async with snow.resource(Incident) as r:
        async for item in r.find({"test": "asdf"}).all(limit=49, offset=0, chunk_size=20):
            print(item)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
