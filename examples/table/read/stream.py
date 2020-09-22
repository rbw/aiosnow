from aiosnow import select
from aiosnow.models.table.declared import IncidentModel as Incident


async def main(client):
    async with Incident(client, table_name="incident") as inc:
        query = select().order_asc(inc.number)

        async for _, record in inc.stream(query, limit=500, page_size=50):
            print("{number} ({sys_id}): {short_description}".format(**record))
