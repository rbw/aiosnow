Declare
-------

Model declaration can be done using :ref:`aiosnow.fields <fields-root>`.


*Example*

.. code-block:: python

    from aiosnow import TableModel, fields

    class Incident(TableModel):
        name = fields.String()
        group = fields.StringMap()
        age = fields.Integer()
        enabled = fields.Boolean()
        created_at = fields.DateTime()

