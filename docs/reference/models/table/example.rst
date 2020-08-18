Example
=======

This example shows how a custom :class:`~aiosnow.models.table.TableSchema` can be used with the :meth:`~aiosnow.Client.get_table`
factory method for producing a :class:`~aiosnow.models.table.TableModel`, for interacting with the *ServiceNow Table API*.

.. code-block:: python

    import asyncio

    import aiosnow
    from aiosnow.models import fields, TableSchema


    class Incident(TableSchema):
        class Meta:
            table_name = "incident"

        sys_id = fields.String(is_primary=True)
        number = fields.String()
        description = fields.String()
        short_description = fields.String()
        priority = fields.IntegerMap()
        impact = fields.IntegerMap()
        assignment_group = fields.StringMap(dump_text=True)
        opened_at = fields.DateTime()


    async def main():
        snow = aiosnow.Client(
            "https://<instance-name>.service-now.com",
            basic_auth=("<username>", "<password>")
        )

        # Produce a TableModel object using a modified IncidentSchema
        async with snow.get_table(Incident) as inc:
            # Get incident with number INC0000001
            response = await inc.get_one(Incident.number == "INC0000001")
            print(response)

    asyncio.run(main())
