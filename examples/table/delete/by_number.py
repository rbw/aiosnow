from aiosnow.models.table.declared import IncidentModel as Incident


async def main(client, q_number: str):
    async with Incident(client, table_name="incident") as inc:
        if await inc.delete(Incident.number == q_number):
            print(f"Successfully deleted {q_number}")
