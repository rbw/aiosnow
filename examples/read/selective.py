from snow import select
from snow.schemas.table import IncidentSchema


class Incident(IncidentSchema):
    class Meta:
        return_only = ["sys_id", "number", "short_description"]


async def main(app):
    async with app.get_table(Incident) as inc:
        query = select(
            Incident.number.starts_with("INC001")
        ).order_asc(Incident.number)

        response = await inc.get(query, limit=10)

        for record in response:
            print(record)
