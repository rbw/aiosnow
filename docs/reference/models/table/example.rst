Example
=======

This example illustrates how a custom :class:`~aiosnow.models.table.TableSchema` can be used with the :meth:`~aiosnow.Client.get_table`
factory method for producing a :class:`~aiosnow.models.table.TableModel`.

.. code-block:: python

    import aiosnow
    from aiosnow.schemas.table import IncidentSchema

    class Incident(IncidentSchema):
        class Meta:
            table_name = "incident"

        sys_id = fields.Text(is_primary=True)
        number = fields.Text()
        description = fields.Text()
        short_description = fields.Text()
        impact = fields.NumericMap()
        assignment_group = fields.TextMap()
        opened_at = fields.DateTime()

    snow = Client(
        "https://<instance-name>.service-now.com",
        basic_auth=("<username>", "<password>")
    )

    # Produce a TableModel object using a modified IncidentSchema
    async with snow.get_table(Incident) as inc:
        # Get incident with number INC01234
        response = await inc.get_one(Incident.number == "INC01234")
        print(response["description"])
