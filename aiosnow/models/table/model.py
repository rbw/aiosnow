import os
from typing import Any, Union

from aiosnow.client import Client
from aiosnow.models import AttachmentModel
from aiosnow.models.attachment.file import FileHandler
from aiosnow.query import Condition, Selector
from aiosnow.request import Response

from .._base.table import BaseTableModel


class TableModel(BaseTableModel):
    def __init__(self, client: Client, attachment: bool = True, **kwargs: Any):
        if attachment:
            self._attachment = AttachmentModel(
                client, table_name=kwargs.get("table_name")
            )

        super(TableModel, self).__init__(client, **kwargs)

    @property
    def _api_url(self) -> Any:
        return f"{self._client.base_url}/api/now/table/{self._table_name}"

    async def upload_file(
        self, selection: Union[Selector, Condition, str], path: str
    ) -> Response:
        """Upload incident attachment

        Args:
            selection: Attachment selection
            path: Source file path

        Returns:
            Response
        """

        path_parts = os.path.split(path)
        record_id = await self.get_object_id(selection)
        return await self._attachment.upload(
            self._table_name or "",
            record_id,
            file_name=path_parts[-1],
            dir_name=os.path.join(*path_parts[:-1]),
        )

    async def download_file(
        self, selection: Union[Selector, Condition, str], dst_dir: str = "."
    ) -> FileHandler:
        """Download incident attachment

        Args:
            selection: Attachment selection
            dst_dir: Destination directory

        Returns:
            FileHandler object
        """

        return await self._attachment.download(selection, dst_dir)

    async def get_attachments(
        self, selection: Union[Selector, Condition, str] = None, **kwargs: Any
    ) -> Response:
        """Returns list of attachments for this table

        Args:
            selection: Attachment selection
            **kwargs: arguments to pass along to AttachmentModel

        Returns:
            Response object
        """

        return await self._attachment.get(
            selection, params=dict(table_name=self._table_name), **kwargs
        )

    async def get_attachment(
        self, selection: Union[Selector, Condition, str] = None, **kwargs: Any
    ) -> Response:
        """Returns Response if the given condition yielded exactly one attachment

        Args:
            selection: Attachment selection
            **kwargs: arguments to pass along to AttachmentModel

        Returns:
            Response object
        """

        return await self._attachment.get_one(
            selection, params=dict(table_name=self._table_name), **kwargs
        )

    async def _close_session(self) -> None:
        await self._close_self()

        if self._attachment:
            await self._attachment._close_session()
