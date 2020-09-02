from pprint import pprint

from aiosnow import fields, select
from aiosnow.schemas.table import IncidentSchema, JournalSchema


class Journal(JournalSchema):
    class Meta:
        return_only = ["element", "sys_created_on", "sys_created_by", "value"]

    element = fields.String(attribute="type")
    sys_created_on = fields.DateTime(attribute="timestamp")
    sys_created_by = fields.String(attribute="author")
    value = fields.String(attribute="message")


class Incident(IncidentSchema):
    class Meta:
        return_only = ["sys_id", "number", "short_description"]


async def main(snow):
    async with snow.get_table(Incident) as inc:
        for response in await inc.get(limit=1):
            record = dict(response)
            async with snow.get_table(Journal) as journal:
                wn_query = select(
                    Journal.element_id.equals(record["sys_id"])
                    & Journal.element.equals("work_notes")
                ).order_asc(Journal.sys_created_on)

                record["journal"] = list(await journal.get(wn_query))

        pprint(record)
