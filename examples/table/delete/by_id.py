from aiosnow.schemas.table import IncidentSchema as Incident


async def main(snow):
    async with snow.get_table(Incident) as inc:
        await inc.delete("636da7ebdb6c1010fba0560868961961")
