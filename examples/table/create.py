from aiosnow.models.table.declared import IncidentModel as Incident


async def main(client):
    async with Incident(client, table_name="incident") as inc:
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
