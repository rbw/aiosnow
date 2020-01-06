import asyncio

from snowstorm.resource import Schema, fields
from snowstorm import Snowstorm, Target, select


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
        selection = select(
            Incident.number.equals("INC0010045")
            # Incident.opened_at.after("2020-01-05 22:35:50")
        ).order_desc(Incident.number)

        async for item in r.stream(selection, limit=5, offset=0, chunk_size=5):
            print(item)

        #result = await r.get(selection, limit=50)
        #print(result)

        #await r.update(selection, data=dict(
        #    short_description="asdf"
        #))

        # print(selection.query)

        # data = await r.create(short_description="asdf", description="asdf123")
        # print(data)


if __name__ == "__main__":
    asyncio.run(main())

