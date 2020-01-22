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
   :undoc-members:
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
