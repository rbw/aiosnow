Declare
-------

Model declaration is done using or or more :ref:`aiosnow.fields <fields-root>` assigned directly
to members of the Model class, or using a separate *ModelSchema* associated via the `model_cls` member.

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

Assign fields using a *ModelSchema* derived class.

.. code-block:: python

    from aiosnow import ModelSchema, TableModel, fields

    class IncidentModelSchema(ModelSchema):
        sys_id = fields.String(is_primary=True)
        number = fields.String()
        impact = fields.IntegerMap()
        priority = fields.Integer()
        assignment_group = fields.StringMap()
        sys_created_on = fields.DateTime()
        made_sla = fields.Boolean()


    class IncidentModel(TableModel):
        schema_cls = IncidentModelSchema
