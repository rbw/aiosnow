import os
from typing import Union

from aiosnow.models import AttachmentModel
from aiosnow.query import Condition, Selector

from .._base.table import BaseTableModel


class TableModel(BaseTableModel):
    def __init__(self, client, **kwargs):
        self._attachment = AttachmentModel(client, table_name=kwargs.get("table_name"))
        super(TableModel, self).__init__(client, **kwargs)

    @property
    def _api_url(self) -> str:
        return self._client.base_url + "/api/now/table/" + self._table_name

    async def upload_file(self, selection: Union[Selector, Condition, str], path):
        path_parts = os.path.split(path)
        record_id = await self.get_object_id(selection)
        return await self._attachment.upload(
            self._table_name,
            record_id,
            file_name=path_parts[-1],
            dir_name=os.path.join(*path_parts[:-1]),
        )

    async def download_file(self, *args, **kwargs):
        return await self._attachment.download(*args, **kwargs)

    async def get_attachments(self, *args, stream=False, **kwargs):
        return await self._attachment.get(*args, **kwargs)

    async def get_attachment(self, selection, **kwargs):
        return await self._attachment.get_one(selection, **kwargs)

    async def _close_session(self):
        await self._close_self()

        if self._attachment:
            await self._attachment._close_session()
