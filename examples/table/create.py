from aiosnow.schemas.table import IncidentSchema as Incident


async def main(snow):
    async with snow.get_table(Incident) as inc:
        response = await inc.create(
            {
                "description": "Incident created using the aiosnow library",
                "short_description": "Test incident",
            }
        )

        print(
            f"Incident created [number: {response['number']}, "
            f"priority: {response['priority'].value}, "
            f"description: {response['description']}]"
        )
