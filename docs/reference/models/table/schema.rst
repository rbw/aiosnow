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

    from aiosnow import Client, fields, model

    class Incident(model.table.TableSchema):
        class Meta:
            table_name = "incident"  # Note

        field1 = fields.Text()

