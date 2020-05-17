from snow.resource import Joined, fields

from .plain import IncidentPlain


class IncidentMapped(IncidentPlain):
    assignment_group = fields.Text(pluck=Joined.DISPLAY_VALUE)
