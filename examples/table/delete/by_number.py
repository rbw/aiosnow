from aiosnow.schemas.table import IncidentSchema as Incident


async def main(app):
    async with app.get_table(Incident) as inc:
        await inc.delete(Incident.number == "INC0010341")
