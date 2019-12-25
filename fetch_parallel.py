import asyncio

from snowstorm.resource import Schema, Text
from snowstorm import Snowstorm


class Incident(Schema):
    __location__ = "/api/now/table/incident"
    __resolve__ = True

    sys_id = Text(required=False)
    number = Text(required=False)
    short_description = Text()

"""



"""


async def main():
    config = dict(
        base_url="https://dev49212.service-now.com",
        username="",
        password=""
    )

    snow = Snowstorm(config)

    async with snow.resource(Incident) as r:
        query = r.build_query(Incident.number.eq("INC0000001") & Incident.sys_id.eq("INC0000002") | Incident.sys_id.eq("INC0000003"))
        print(query.raw)

        #async for item in r.select(query).all(limit=1, offset=0, chunk_size=5):
        #    print(item)

        # await r.select_native({"test": "asdf"}).update({"test": "bajs"})

        #await r.create(
        #    short_description="test"
        #)


if __name__ == "__main__":
    asyncio.run(main())

