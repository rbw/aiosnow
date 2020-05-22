Schema
======

The TableSchema functions like a regular schema, but requires :attr:`~snow.models.table.TableSchema.Meta.table_name`
to be set in the :class:`~snow.models.table.TableSchema.Meta` inner class.


API
---

.. automodule:: snow.models.table
   :members: TableSchema


Example
-------

.. code-block:: python

    from snow import Snow, fields, model

    class Incident(model.table.TableSchema):
        class Meta:
            table_name = "incident"

        field1 = fields.Text()

