from aiosnow import ModelSchema, TableModel, fields, select


def test_query_single():
    class Incident(TableModel):
        sys_id = fields.String()
        number = fields.String()

    assert str(Incident.number == "number123") == "number=number123"


def test_query_builder_and():
    class Incident(TableModel):
        number = fields.String()
        priority = fields.Integer()

    sysparm_query = select(
        Incident.number.equals("number123") & Incident.priority.less_than(2)
    )
    assert str(sysparm_query) == "number=number123^priority<2"


def test_query_builder_or():
    class Incident(TableModel):
        sys_id = fields.String()
        impact = fields.Integer()

    sysparm_query = select(Incident.sys_id.equals("id123") | Incident.impact.equals(5))
    assert str(sysparm_query) == "sys_id=id123^ORimpact=5"


def test_query_builder_nested():
    class AssignmentGroup(ModelSchema):
        sys_id = fields.String()
        name = fields.String()

    class Incident(TableModel):
        number = fields.String()
        assignment_group = AssignmentGroup

    assert (
        str(Incident.assignment_group.name == "test123")
        == "assignment_group.name=test123"
    )
    assert (
        str(Incident.assignment_group.name.equals("test321"))
        == "assignment_group.name=test321"
    )
    assert (
        str(Incident.assignment_group.sys_id == "id123")
        == "assignment_group.sys_id=id123"
    )

    assert (
        str(
            select(
                Incident.assignment_group.name.equals("test")
                & Incident.number.ends_with("01")
            )
        )
        == "assignment_group.name=test^numberENDSWITH01"
    )


def test_query_builder_nq():
    class Incident(TableModel):
        priority = fields.Integer()
        impact = fields.Integer()

    assert (
        str(
            select(
                Incident.priority.equals(2) & Incident.impact.equals(5)
                ^ Incident.impact.not_equals(1)
                | Incident.priority.equals(2)
            )
        )
        == "priority=2^impact=5^NQimpact!=1^ORpriority=2"
    )
