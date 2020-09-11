Example
=======

Custom :class:`~aiosnow.models.table.TableModel` class for working with incidents.

.. code-block:: python

    import asyncio
    import aiosnow
    from aiosnow.models import TableModel, fields


    class Incident(TableModel):
        sys_id = fields.String(is_primary=True)
        number = fields.String()
        description = fields.String()
        short_description = fields.String()
        priority = fields.IntegerMap()
        impact = fields.IntegerMap()
        assignment_group = fields.StringMap(dump_text=True)
        opened_at = fields.DateTime()


    async def main():
        client = aiosnow.Client(
            "https://<instance-name>.service-now.com",
            basic_auth=("<username>", "<password>")
        )

        async with Incident(client, table_name="incident") as inc:
            response = await inc.get_one(Incident.number == "INC0000001")
            print(response.data)


    asyncio.run(main())
