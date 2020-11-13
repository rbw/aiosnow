from .._schema import fields


class AttachmentModelSchema:
    """Attachment API model schema"""

    sys_id = fields.String(is_primary=True)
    table_name = fields.String()
    file_name = fields.String()
    size_bytes = fields.Integer()
    sys_mod_count = fields.String()
    average_image_color = fields.String()
    image_width = fields.String()
    sys_updated_on = fields.DateTime()
    sys_tags = fields.String()
    image_height = fields.String()
    sys_updated_by = fields.String()
    download_link = fields.String()
    content_type = fields.String()
    sys_created_on = fields.DateTime()
    size_compressed = fields.String()
    compressed = fields.Boolean()
    state = fields.String()
    table_sys_id = fields.String()
    chunk_size_bytes = fields.String()
    hash = fields.String()
    sys_created_by = fields.String()
