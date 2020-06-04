from snow.schemas.table import IncidentSchema as Incident


async def main(app):
    async with app.get_table(Incident) as inc:
        await inc.delete("636da7ebdb6c1010fba0560868961961")
