from snow.model import fields
from snow.schemas.table import IncidentSchema


class Incident(IncidentSchema):
    priority = fields.IntegerMap()


async def main(app):
    async with app.get_table(Incident) as inc:
        response = await inc.create(
            {
                "description": "Incident created using the Snow library",
                "short_description": "Test incident",
            }
        )

        print(
            f"Incident created [number: {response['number']}, "
            f"priority: {response['priority'].text}, "
            f"description: {response['description']}]"
        )
