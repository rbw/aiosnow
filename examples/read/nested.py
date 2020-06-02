from snow import fields, PartialSchema, select
from snow.schemas.table import IncidentSchema


class AssignmentGroup(PartialSchema):
    sys_id = fields.Text()
    name = fields.Text()


class Incident(IncidentSchema):
    number = fields.Text()
    impact = fields.Numeric()
    assignment_group = AssignmentGroup


async def main(app):
    async with app.get_table(Incident) as inc:
        query = select(
            Incident.assignment_group.name.equals("Hardware")
            & Incident.impact.greater_or_equals(1)
        ).order_asc(Incident.number)

        async for _, record in inc.stream(query, limit=194, page_size=43):
            ag = record["assignment_group"]
            text = "{number} is assigned to group: {ag_name} ({ag_id})".format(
                number=record["number"],
                ag_id=ag["sys_id"],
                ag_name=ag["name"]
            )
            print(text)
