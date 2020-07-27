Schema
======

The TableSchema behaves like a regular schema, but requires :attr:`~aiosnow.models.table.TableSchema.Meta.table_name`
to be set in the :class:`~aiosnow.models.table.TableSchema.Meta` inner class.


API
---

.. automodule:: aiosnow.models.table
   :members: TableSchema


Example
-------

.. code-block:: python

    from aiosnow.models.common.schema import fields
    from aiosnow.models.table import TableSchema


    class Incident(TableSchema):
        class Meta:
            table_name = "incident"

        sys_id = fields.String(is_primary=True)
        number = fields.String()
        description = fields.String()
        short_description = fields.String()
        impact = fields.IntegerMap()
        assignment_group = fields.StringMap()
        opened_at = fields.DateTime()
