.. _reference-schema:

Schema
======

Schemas are used for:
    - Defining Resources
    - Building queries
    - Request payload serialization
    - Response content deserialization
    - Validation


.. automodule:: snow.resource.schema
   :members: Schema
   :exclude-members: opts, OPTIONS_CLASS


*Example – Incident Schema*

.. code-block:: python

    from snow.resource import Schema, fields


    class Incident(Schema):
        __location__ = "/api/now/table/incident"

        sys_id = fields.Text(is_primary=True)
        number = fields.Text()
        description = fields.Text()
        short_description = fields.Text()
        priority = fields.Numeric()
        assignment_group = fields.Text(pluck=Joined.DISPLAY_VALUE)
        opened_at = fields.Datetime()

Nesting
*******

Schemas can be nested using the PartialSchema class.
When used with a Resource, related objects are automatically resolved.

.. code-block:: python

    class AssignmentGroup(PartialSchema):
        name = fields.Text()
        manager = fields.Text()

    class Incident(Schema):
        __location__ = "/api/now/table/incident"

        sys_id = fields.Text(is_primary=True)
        number = fields.Text()
        description = fields.Text()
        short_description = fields.Text()
        impact = fields.Numeric()
        assignment_group = AssignmentGroup
        opened_at = fields.Datetime()

Fields
******

Schema Fields are classes used when defining a Schema, which is used in (de)serialization, validation,
selection and more. Also, once instantiated, the field becomes compatible with the Snow query system.

.. toctree::

    fields
