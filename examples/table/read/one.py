from aiosnow.models.table.declared import IncidentModel as Incident


async def main(client, q_number: str):
    async with Incident(client, table_name="incident") as i:
        response = await i.get_one(Incident.number == q_number)
        print(response["description"])
