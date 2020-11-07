from aiosnow import select, ModelSchema, fields
from aiosnow.models.table.declared import IncidentModel


class AssignmentGroup(ModelSchema):
    sys_id = fields.String()
    name = fields.String()


class Incident(IncidentModel):
    assignment_group = AssignmentGroup


async def main(client):
    query = select(
        Incident.assignment_group.name.equals("Hardware")
        & Incident.impact.greater_or_equals(1)
    ).order_asc(Incident.number)

    async with Incident(client, table_name="incident") as api:
        for response in await api.get(query, limit=1):
            agrp = response["assignment_group"]
            print(
                "{number} ({sys_id}) is assigned to group: {ag_name} ({ag_id})".format(
                    sys_id=response["sys_id"],
                    number=response["number"],
                    ag_id=agrp["sys_id"],
                    ag_name=agrp["name"],
                )
            )
