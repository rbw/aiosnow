from snow.schemas.table import IncidentSchema as Incident


async def main(app):
    async with app.get_table(Incident) as inc:
        response = await inc.get_one(Incident.number == "INC0010240")
        print(response["description"])
