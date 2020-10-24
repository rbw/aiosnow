from .base import BaseTableModel


class TableModel(BaseTableModel):
    def __init__(self, *args, **kwargs):
        super(TableModel, self).__init__(*args, **kwargs)

    @property
    def _api_url(self) -> str:
        return self._client.base_url + "/api/now/table/" + self._table_name
