import asyncio

from snowstorm.resource import Schema, fields
from snowstorm import Snowstorm, Target


class Incident(Schema):
    __location__ = "/api/now/table/incident"

    sys_id = fields.Text()
    number = fields.Text()
    description = fields.Text(required=True)
    short_description = fields.Text(required=True)
    impact = fields.Text(target=Target.DISPLAY_VALUE)
    assignment_group = fields.Text(target=Target.DISPLAY_VALUE)
    opened_at = fields.Datetime()


async def main():
    config = dict(
        base_url="https://dev49212.service-now.com",
        username="",
        password=""
    )

    snow = Snowstorm(config)

    async with snow.resource(Incident) as r:
        reader = (
            r.select(
                # Incident.number.equals("INC0010029") &
                Incident.opened_at.after("2019-12-24 00:01:02")
            )
            .order_desc(Incident.number)
        )

        async for item in reader.stream(limit=5, offset=0, chunk_size=5):
            print(item)

        #data = await r.create(short_description="asdf", description="asdf123")
        #print(data)


if __name__ == "__main__":
    asyncio.run(main())

