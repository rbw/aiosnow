import asyncio

from typing import Union
from concurrent.futures import ThreadPoolExecutor

from aiosnow.models.common import fields
from aiosnow.models.table import TableModel
from aiosnow.request import methods
from aiosnow.query import Condition, Selector

from .file import FileWriter


class AttachmentModel(TableModel):
    """Attachment API model"""

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
    size_compressed = fields.Integer()
    compressed = fields.Boolean()
    state = fields.String()
    table_sys_id = fields.String()
    chunk_size_bytes = fields.String()
    hash = fields.String()
    sys_created_by = fields.String()

    def __init__(self, *args, **kwargs):
        self.io_pool_exc = ThreadPoolExecutor(max_workers=10)
        self.loop = asyncio.get_running_loop()
        super(AttachmentModel, self).__init__(*args, table_name="", **kwargs)

    @property
    def _api_url(self) -> str:
        return self._client.base_url + "/api/now/attachment"

    async def download(self, selection: Union[Selector, Condition, str], dst_dir="."):
        attachment = await self.get_one(selection)
        response = await self._session.request(
            methods.GET,
            url=attachment["download_link"],
            headers={"Content-type": attachment["content_type"], "Accept": "*/*"},
        )
        file = FileWriter(attachment["file_name"])
        with file as f:
            # The idea here is to fetch chunks of data as yielded
            # by the API and write directly to the file's buffer.
            async for data_chunk, _ in response.content.iter_chunks():
                await self.loop.run_in_executor(self.io_pool_exc, f.write, data_chunk)

        return file

    async def upload(self):
        pass
