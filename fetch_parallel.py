import asyncio

from snowstorm.resource import Schema, fields
from snowstorm import Client, Joined, select


class Incident(Schema):
    __location__ = "/api/now/table/incident"

    sys_id = fields.Text(is_primary=True)
    number = fields.Text()
    description = fields.Text()
    short_description = fields.Text()
    impact = fields.Numeric(pluck=Joined.DISPLAY_VALUE)
    priority = fields.Numeric(pluck=Joined.DISPLAY_VALUE)
    assignment_group = fields.Text(pluck=Joined.DISPLAY_VALUE)
    opened_at = fields.Datetime()


async def main():
    config = dict(
        address="https://dev49212.service-now.com",
        username="",
        password=""
    )

    snow = Client(config)

    async with snow.resource(Incident) as r:
        selection = select(
            # Incident.number.equals("INC0010120")
            # Incident.opened_at.after("2020-01-05 22:35:50")
        ).order_desc(Incident.number)

        # Get the
        await r.get(limit=50)

        async for item in r.stream(selection, limit=0, offset=0, chunk_size=5):
            print(item)

        data = await r.create({
            Incident.short_description: "a",
            Incident.description: "test"
        })

        print(data)

        #deleted = await r.delete(data["sys_id"])
        #print(deleted)

        data = await r.update(
            data["sys_id"],
            {
                Incident.description: "hello",
                Incident.impact: 2,
                Incident.priority: 1
            }
        )

        print(data)


if __name__ == "__main__":
    asyncio.run(main())

