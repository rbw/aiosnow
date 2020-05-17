from snow.resource import PartialSchema, fields

from .plain import IncidentPlain


class AssignmentGroup(PartialSchema):
    sys_id = fields.Text()
    name = fields.Text()


class IncidentExpanded(IncidentPlain):
    assignment_group = AssignmentGroup
