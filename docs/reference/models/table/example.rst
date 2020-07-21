Example
=======

This example illustrates how a custom :class:`~aiosnow.models.table.TableSchema` can be used with the :meth:`~aiosnow.Client.get_table`
factory method for producing a :class:`~aiosnow.models.table.TableModel`.

.. code-block:: python

    from aiosnow import Client, model

    class Incident(model.schema.TableSchema):
        class Meta:
            table_name = "incident"

        sys_id = fields.Text(is_primary=True)
        number = fields.Text()
        description = fields.Text()
        short_description = fields.Text()
        impact = fields.NumericMap()
        assignment_group = fields.TextMap()
        opened_at = fields.DateTime()

    app = Client(
        "https://my-instance.service-now.com",
        basic_auth=("<username>", "<password>")
    )

    # Produce a TableModel object using the built-in Incident schema
    async with app.get_table(Incident) as r:
        # Get incident with number INC01234
        response = await r.get_one(Incident.number == "INC01234")
        print(response["description"])

