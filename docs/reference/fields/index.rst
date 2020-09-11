.. _fields-root:

Fields
======

The :ref:`aiosnow.fields <fields-root>` module provides a set of typed classes for:

    1) Defining schemas
    2) Building queries
    3) Serializing data

*Example, schema definition & querying*

.. code-block:: python

    import aiosnow
    from aiosnow.models import fields, TableModel


    class Incident(TableModel):
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
