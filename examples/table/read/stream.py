from aiosnow import select
from aiosnow.schemas.table import IncidentSchema as Incident


async def main(snow):
    async with snow.get_table(Incident) as inc:
        query = select(Incident.number.starts_with("INC001")).order_asc(Incident.number)

        async for _, record in inc.stream(query, limit=500, page_size=50):
            print(record["number"], record["short_description"])
