import asyncio

from snowstorm.resource import Resource, ResourceSchema, fields


class Incident(ResourceSchema):
    __location__ = "/api/now/table/incident"

    number = fields.String()
    sys_id = fields.String()


async def get_many():
    async with Resource(Incident) as incidents:
        async for record in incidents.find({"test": "asdf"}).all():
            #print(record)
            pass


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_many())
