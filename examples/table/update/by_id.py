from aiosnow.schemas.table import IncidentSchema as Incident


async def main(snow):
    async with snow.get_table(Incident) as inc:
        response = await inc.update("01b9e36bdb6c1010fba0560868961925", {"impact": 1})

        print(
            f"Updated: {response['number']} ({response['sys_id']}), "
            f"new impact: {response['impact'].value}"
        )
