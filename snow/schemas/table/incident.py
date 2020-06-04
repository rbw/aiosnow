from snow.model import fields
from snow.models.table import TableSchema


class IncidentSchema(TableSchema):
    class Meta:
        table_name = "incident"

    sys_id = fields.String(is_primary=True)
    impact = fields.Integer()
    number = fields.String()
    parent = fields.String()
    made_sla = fields.Boolean()
    caused_by = fields.String()
    watch_list = fields.String()
    upon_reject = fields.String()
    sys_updated_on = fields.DateTime()
    child_incidents = fields.Integer()
    hold_reason = fields.Integer()
    approval_history = fields.String()
    resolved_by = fields.String()
    sys_updated_by = fields.String()
    opened_by = fields.String()
    user_input = fields.String()
    sys_created_on = fields.DateTime()
    sys_domain = fields.String()
    state = fields.Integer()
    sys_created_by = fields.String()
    knowledge = fields.Boolean()
    order = fields.Integer()
    calendar_stc = fields.Integer()
    closed_at = fields.DateTime()
    cmdb_ci = fields.String()
    delivery_plan = fields.String()
    active = fields.Boolean()
    work_notes_list = fields.String()
    business_service = fields.String()
    priority = fields.Integer()
    sys_domain_path = fields.String()
    rfc = fields.String()
    time_worked = fields.Integer()
    expected_start = fields.DateTime()
    opened_at = fields.DateTime()
    business_duration = fields.DateTime()
    group_list = fields.String()
    work_end = fields.DateTime()
    reopened_time = fields.DateTime()
    resolved_at = fields.DateTime()
    caller_id = fields.String()
    approval_set = fields.DateTime()
    subcategory = fields.String()
    work_notes = fields.String()
    short_description = fields.String()
    close_code = fields.String()
    correlation_display = fields.String()
    work_start = fields.DateTime()
    delivery_task = fields.String()
    assignment_group = fields.String()
    business_stc = fields.Integer()
    additional_assignee_list = fields.String()
    description = fields.String()
    calendar_duration = fields.DateTime()
    notify = fields.Integer()
    sys_class_name = fields.String()
    close_notes = fields.String()
    closed_by = fields.String()
    follow_up = fields.DateTime()
    parent_incident = fields.String()
    contact_type = fields.String()
    reopened_by = fields.String()
    incident_state = fields.Integer()
    urgency = fields.Integer()
    problem_id = fields.String()
    company = fields.String()
    reassignment_count = fields.Integer()
    activity_due = fields.DateTime()
    assigned_to = fields.String()
    severity = fields.Integer()
    comments = fields.String()
    sla_due = fields.DateTime()
    approval = fields.String()
    comments_and_work_notes = fields.String()
    due_date = fields.DateTime()
    sys_mod_count = fields.Integer()
    reopen_count = fields.Integer()
    sys_tags = fields.String()
    escalation = fields.Integer()
    upon_approval = fields.String()
    correlation_id = fields.String()
    location = fields.String()
    category = fields.String()
