import asyncio
from concurrent.futures import ThreadPoolExecutor
from mimetypes import guess_type
from typing import Any, Union

from aiosnow.models.common import fields
from aiosnow.models.table import BaseTableModel
from aiosnow.query import Condition, Selector
from aiosnow.request import methods
from aiosnow.request.response import ClientResponse, Response

from .file import FileHandler, FileReader, FileWriter


class AttachmentModel(BaseTableModel):
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
    size_compressed = fields.String()
    compressed = fields.Boolean()
    state = fields.String()
    table_sys_id = fields.String()
    chunk_size_bytes = fields.String()
    hash = fields.String()
    sys_created_by = fields.String()

    def __init__(self, *args, **kwargs):
        self.io_pool_exc = ThreadPoolExecutor(max_workers=10)
        self.loop = asyncio.get_running_loop()
        super(AttachmentModel, self).__init__(*args, **kwargs)

    @property
    def _api_url(self) -> str:
        return self._client.base_url + "/api/now/attachment"

    async def download(
        self, selection: Union[Selector, Condition, str], dst_dir: str = "."
    ) -> FileHandler:
        print(selection)
        meta = await self.get_one(selection)
        data = await self.request(
            methods.GET,
            url=meta["download_link"],
            headers={"Content-type": meta["content_type"]},
        )
        with FileWriter(meta["file_name"], dst_dir) as f:
            await self.loop.run_in_executor(
                self.io_pool_exc, f.write, await data.read()
            )

        return f

    async def update(self, selection: Union[Condition, str], payload: dict) -> Response:
        pass

    async def upload(
        self, table_name: str, record_sys_id: str, file_name: str, **kwargs: Any
    ) -> ClientResponse:
        with FileReader(file_name, **kwargs) as f:
            content = await self.loop.run_in_executor(self.io_pool_exc, f.read)

        content_type, _ = guess_type(file_name)
        response = await self.request(
            methods.POST,
            url=f"{self._api_url}/file",
            params=dict(
                table_name=table_name, table_sys_id=record_sys_id, file_name=file_name
            ),
            headers={"Content-type": content_type},
            payload=content,
        )
        return response
