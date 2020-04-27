from snow.exceptions import RequestError
from snow.request import DeleteRequest

from .base import RequestHelper


class Deleter(RequestHelper):
    @property
    def schema(self):
        return

    async def delete(self, object_id):
        response, content = await DeleteRequest(self.resource, object_id).send()
        if response.status == 204:
            return dict(result="success")
        else:
            raise RequestError(
                f"Unexpected response for DELETE request. "
                f"Status: {response.status}, Text: {content}",
                response.status,
            )
