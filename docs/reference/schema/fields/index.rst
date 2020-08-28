.. _fields-root:

Fields
======

The field classes serves two purposes. First, they are used when defining schemas. Second, they can be used for building queries.

*Example, schema definition & querying*

.. code-block:: python

    import aiosnow
    from aiosnow.models import fields, TableSchema


    class Incident(TableSchema):
        class Meta:
            table_name = "incident"

        sys_id = fields.String(is_primary=True)
        number = fields.String()
        description = fields.String()
        priority = fields.IntegerMap()
        impact = fields.IntegerMap()
        assignment_group = fields.StringMap(dump_text=True)
        opened_at = fields.DateTime()

    # Get incidents starting with "INC123", with priority greater than 2
    query = aiosnow.select(
        Incident.number.starts_with("INC123")
        &
        Incident.priority.greater_than(2)
    )

    [...]


.. toctree::
   :maxdepth: 2

   string
   integer
   datetime
   boolean
   integermap
   stringmap
