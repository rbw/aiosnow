.. _reference-schema:

Schema
======

Schemas are used for:
    - Defining Resources
    - Building queries
    - Request payload serialization
    - Response content deserialization
    - Validation

The library comes with a set of standard schemas, available in *snow.schemas*.


.. automodule:: snow.resource.schema
   :members: Schema
   :exclude-members: opts, OPTIONS_CLASS


*Example – Incident Schema*

.. code-block:: python

    from snow.resource import Schema, fields


    class Incident(Schema):
        class Meta:
            location = "/api/now/table/incident"

        sys_id = fields.Text(is_primary=True)
        number = fields.Text()
        description = fields.Text()
        short_description = fields.Text()
        priority = fields.Numeric()
        assignment_group = fields.Text(pluck=Joined.DISPLAY_VALUE)
        opened_at = fields.Datetime()

Nesting
*******

Schemas can be nested using the :class:`~snow.resource.schema.PartialSchema` class.
When used with a Resource, related objects are automatically resolved.

.. code-block:: python

    class AssignmentGroup(PartialSchema):
        name = fields.Text()
        manager = fields.Text()

    class Incident(Schema):
        class Meta:
            location = "/api/now/table/incident"

        sys_id = fields.Text(is_primary=True)
        number = fields.Text()
        description = fields.Text()
        short_description = fields.Text()
        impact = fields.Numeric()
        assignment_group = AssignmentGroup
        opened_at = fields.Datetime()

