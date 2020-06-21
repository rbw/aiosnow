Partial
=======

Schemas can be nested with the special :class:`~snow.model.schema.PartialSchema` class, which doesn't require a
Meta inner class.

When registered as a field, as illustrated in the example below, the nested fields can be queried as well.

Example
-------

TableSchema with nested assignment_group

.. code-block:: python

    from snow.model.schema import TableSchema, PartialSchema, fields

    class AssignmentGroup(PartialSchema):
        name = fields.Text()
        manager = fields.Text()

    class Incident(TableSchema):
        class Meta:
            table_name = "incident"

        sys_id = fields.Text(is_primary=True)
        number = fields.Text()
        description = fields.Text()
        short_description = fields.Text()
        impact = fields.Numeric()
        assignment_group = AssignmentGroup
        opened_at = fields.DateTime()
