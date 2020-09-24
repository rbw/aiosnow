Declare
-------

Model declaration is done using :ref:`aiosnow.fields <fields-root>`.


*Example*

.. code-block:: python

    from aiosnow import TableModel, fields

    class Incident(TableModel):
        sys_id = fields.String(is_primary=True)
        number = fields.String()
        impact = fields.IntegerMap()
        priority = fields.Integer()
        assignment_group = fields.StringMap()
        sys_created_on = fields.DateTime()
        made_sla = fields.Boolean()
