Example
=======

This example illustrates how a custom :class:`~snow.model.schema.table.TableSchema` can be used with the :meth:`~snow.Snow.get_table`
factory method for producing a :class:`~snow.model.table.TableModel`.

.. code-block:: python

    from snow import Snow, model

    class Incident(model.schema.TableSchema):
        class Meta:
            table_name = "incident"

        sys_id = fields.Text(is_primary=True)
        number = fields.Text()
        description = fields.Text()
        short_description = fields.Text()
        impact = fields.NumericMap()
        assignment_group = fields.TextMap()
        opened_at = fields.Datetime()

    app = Snow(
        "https://my-instance.service-now.com",
        basic_auth=("<username>", "<password>")
    )

    # Product a TableModel object using the built-in Incident schema
    async with app.get_table(Incident) as r:
        # Get incident with number INC01234
        response = await r.get_one(Incident.number == "INC01234")
        print(response["description"])

