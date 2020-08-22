from aiosnow.schemas.table import IncidentSchema as Incident


async def main(app):
    async with app.get_table(Incident) as inc:
        response = await inc.update(Incident.number == "INC0010380", {"impact": 1})

        print(
            f"Updated: {response['number']} ({response['sys_id']}),"
            f"new impact: {response['impact'].value}"
        )
