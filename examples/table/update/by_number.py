from aiosnow.models.table.declared import IncidentModel as Incident


async def main(client, q_number: str):
    async with Incident(client, table_name="incident") as inc:
        response = await inc.update(Incident.number == q_number, {"impact": 1})

        print(
            f"Updated: {response['number']} ({response['sys_id']}),"
            f"new impact: {response['impact'].value}"
        )
