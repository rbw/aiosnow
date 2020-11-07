from aiosnow import select, fields
from aiosnow.models.table.declared import IncidentModel as Incident, JournalModel


class Journal(JournalModel):
    element = fields.String(attribute="type")
    sys_created_on = fields.DateTime(attribute="timestamp")
    sys_created_by = fields.String(attribute="author")
    value = fields.String(attribute="message")


async def main(client, q_number: str):
    async with Incident(
        client,
        table_name="incident",
        return_only=["sys_id", "number", "short_description"],
    ) as inc:
        response = await inc.get_one(Incident.number == q_number)
        record = response.data
        async with Journal(
            client,
            table_name="sys_journal_field",
            return_only=["element", "sys_created_on", "sys_created_by", "value"],
        ) as jnl:
            wn_query = select(
                Journal.element_id.equals(record["sys_id"])
                & Journal.element.equals("work_notes")
            ).order_asc(Journal.sys_created_on)

            record["journal"] = list(await jnl.get(wn_query))

        print(record)
