import asyncio

from snowstorm.resource import Schema, fields
from snowstorm import Snowstorm, Target


class Incident(Schema):
    __location__ = "/api/now/table/incident"

    sys_id = fields.Text()
    number = fields.Text()
    description = fields.Text()
    short_description = fields.Text()
    impact = fields.Text(target=Target.DISPLAY_VALUE)
    assignment_group = fields.Text(target=Target.DISPLAY_VALUE)
    opened_at = fields.Datetime()


async def main():
    config = dict(
        address="https://dev49212.service-now.com",
        username="",
        password=""
    )

    snow = Snowstorm(config)

    async with snow.resource(Incident) as r:
        from datetime import datetime, timedelta

        reader = (
            r.select(
                # Incident.number.equals("INC0010029") &
                Incident.opened_at.after("2020-01-04 23:36:58")
            )
            .order_desc(Incident.number)
        )

        async for item in reader.stream(limit=5, offset=0, chunk_size=5):
            print(item)

        # data = await r.create(short_description="asdf", description="asdf123")
        # print(data)


if __name__ == "__main__":
    asyncio.run(main())

