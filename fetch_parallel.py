import asyncio

from snowstorm.resource import Schema, fields
from snowstorm import Snowstorm


class Incident(Schema):
    __location__ = "/api/now/table/incident"
    __resolve__ = True

    sys_id = fields.String(required=False)
    number = fields.String(required=False)
    short_description = fields.String()


async def main():
    config = dict(
        base_url="https://dev49212.service-now.com",
        username="",
        password=""
    )

    snow = Snowstorm(config)

    async with snow.resource(Incident) as r:
        query = {"test": "asdf"}

        async for item in r.find(query).all(limit=60, offset=0, chunk_size=10):
            print(item)

        await r.create(
            short_description="test"
        )


if __name__ == "__main__":
    asyncio.run(main())
