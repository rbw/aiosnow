from aiosnow.schemas.table import IncidentSchema as Incident


async def main(snow):
    async with snow.get_table(Incident) as inc:
        response = await inc.get_one(Incident.number == "INC0010240")
        print(response["description"])
