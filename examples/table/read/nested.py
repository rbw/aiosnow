from aiosnow import fields, PartialSchema, select
from aiosnow.schemas.table import IncidentSchema


class AssignmentGroup(PartialSchema):
    sys_id = fields.String()
    name = fields.String()


class Incident(IncidentSchema):
    assignment_group = AssignmentGroup


async def main(app):
    async with app.get_table(Incident) as inc:
        query = select(
            Incident.assignment_group.name.equals("Hardware")
            & Incident.impact.greater_or_equals(1)
        ).order_asc(Incident.number)

        for response in await inc.get(query):
            ag = response["assignment_group"]
            print(
                "{number} is assigned to group: {ag_name} ({ag_id})".format(
                    number=response["number"], ag_id=ag["sys_id"], ag_name=ag["name"]
                )
            )
