import asyncio

from snowstorm.resource import Schema, Text
from snowstorm import Snowstorm


class Incident(Schema):
    __location__ = "/api/now/table/incident"
    __resolve__ = True

    sys_id = Text()
    number = Text()
    short_description = Text(required=True)


async def main():
    config = dict(
        base_url="https://dev49212.service-now.com",
        username="",
        password=""
    )

    snow = Snowstorm(config)

    async with snow.resource(Incident) as r:
        query = Incident.number.eq("INC0000060") | Incident.number.eq("INC0000059")

        #async for item in r.select(query).stream(limit=5, offset=0, chunk_size=5):
        #    print(item)

        await r.create(short_description="asdf")

if __name__ == "__main__":
    asyncio.run(main())

