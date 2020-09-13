from aiosnow.models.table.declared import IncidentModel as Incident


async def main(client, q_sys_id: str):
    async with Incident(client, table_name="incident") as inc:
        response = await inc.update(q_sys_id, {"impact": 1})

        print(
            f"Updated: {response['number']} ({response['sys_id']}), "
            f"new impact: {response['impact'].value}"
        )
