import asyncio

from snowstorm.resource import Schema, Text
from snowstorm import Snowstorm


class Incident(Schema):
    __location__ = "/api/now/table/incident"
    __related__ = True

    sys_id = Text()
    number = Text()
    description = Text(required=True)
    short_description = Text(required=True)


async def main():
    config = dict(
        base_url="https://dev49212.service-now.com",
        username="",
        password=""
    )

    snow = Snowstorm(config)

    async with snow.resource(Incident) as r:
        request = (
            r.select(
                Incident.number.eq("INC0000060") |
                Incident.number.eq("INC0000059")
            )
            .order_desc([Incident.number, Incident.description])
            .order_asc(Incident.description)
        )

        async for item in request.stream(limit=5, offset=0, chunk_size=5):
            print(item)

        #data = await r.create(short_description="asdf", description="asdf123")
        #print(data)


if __name__ == "__main__":
    asyncio.run(main())

