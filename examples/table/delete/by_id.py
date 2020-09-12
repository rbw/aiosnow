from aiosnow.models.table.builtins import IncidentModel as Incident


async def main(client, q_sys_id: str):
    async with Incident(client, table_name="incident") as inc:
        if await inc.delete(q_sys_id):
            print(f"Successfully deleted {q_sys_id}")
