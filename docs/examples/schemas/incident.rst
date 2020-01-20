.. _example-schema-incident:

Example
-------

.. code-block:: python

    from snow.resource import Schema, fields


    class Incident(Schema):
        __location__ = "/api/now/table/incident"

        sys_id = fields.Text(is_primary=True)
        number = fields.Text()
        description = fields.Text()
        short_description = fields.Text()
        impact = fields.Numeric(pluck=Joined.DISPLAY_VALUE)
        priority = fields.Numeric(pluck=Joined.DISPLAY_VALUE)
        assignment_group = fields.Text(pluck=Joined.DISPLAY_VALUE)
        opened_at = fields.Datetime()
