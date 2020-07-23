Partial
=======

Schemas can be nested with the special :class:`~aiosnow.model.schema.PartialSchema` class, which doesn't require a
Meta inner class.


Example
-------

TableSchema with nested assignment_group

.. code-block:: python

    from aiosnow.model.schema import PartialSchema, fields
    from aiosnow.schemas.table.incident import IncidentSchema

    class AssignmentGroup(PartialSchema):
        name = fields.Text()
        manager = fields.Text()

    class Incident(IncidentSchema):
        assignment_group = AssignmentGroup  # override with a partial schema
