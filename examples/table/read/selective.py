from aiosnow import select
from aiosnow.models.table.builtins import IncidentModel as Incident


async def main(client, q_number: str):
    async with Incident(
        client,
        table_name="incident",
        return_only=["sys_id", "number", "short_description"],
    ) as inc:
        query = select(inc.number.equals(q_number)).order_asc(inc.number)

        for record in await inc.get(query, limit=10):
            print(record)
