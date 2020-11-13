Declare
-------

The Model Declaration is done by making one or more :ref:`aiosnow.fields <fields-root>` members of the Model.

Model
*****

Assign fields directly on the *BaseModel* derived class.

.. code-block:: python

    from aiosnow import TableModel, fields

    class IncidentModel(TableModel):
        sys_id = fields.String(is_primary=True)
        number = fields.String()
        impact = fields.IntegerMap()
        priority = fields.Integer()
        assignment_group = fields.StringMap()
        sys_created_on = fields.DateTime()
        made_sla = fields.Boolean()




ModelSchema
***********

Assign fields in separate class, which is then subclassed.

.. code-block:: python

    from aiosnow import TableModel, fields

    class IncidentModelSchema:
        sys_id = fields.String(is_primary=True)
        number = fields.String()
        impact = fields.IntegerMap()
        priority = fields.Integer()
        assignment_group = fields.StringMap()
        sys_created_on = fields.DateTime()
        made_sla = fields.Boolean()


    class IncidentModel(TableModel, IncidentModelSchema):
        """Incident API Model"""
