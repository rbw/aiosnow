Partial
=======

Schemas can be nested with the special :class:`~aiosnow.models.common.schema.PartialSchema` class, which doesn't require a
Meta inner class.


Example
-------

Override assignment_group of :class:`~aiosnow.schemas.table.IncidentSchema`.

.. code-block:: python

    from aiosnow.models.common.schema import PartialSchema, fields
    from aiosnow.schemas.table.incident import IncidentSchema

    class AssignmentGroup(PartialSchema):
        name = fields.String()
        manager = fields.String()

    class Incident(IncidentSchema):
        assignment_group = AssignmentGroup
