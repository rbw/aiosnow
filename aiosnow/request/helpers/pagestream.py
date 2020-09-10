from typing import Any, AsyncGenerator

from aiosnow.consts import DEFAULT_LIMIT, DEFAULT_PAGE_SIZE
from aiosnow.request import GetRequest


class Pagestream(GetRequest):
    """Aiosnow Pagestream

    The Pagestream object behaves much like a stream, it's memory friendly and yields deserialized
    chunks of records using the ServiceNow pagination system.

    Attributes:
        page_size (int): Number of records in each page
    """

    exhausted = False

    def __init__(self, *args: Any, page_size: int = DEFAULT_PAGE_SIZE, **kwargs: Any):
        self._limit_total = kwargs.pop("limit", DEFAULT_LIMIT)
        self._offset_initial = kwargs.get("offset", 0)
        super(Pagestream, self).__init__(*args, **kwargs)
        self._limit = page_size

    def __repr__(self) -> str:
        params = (
            f"query: {self.query or None}, limit: {self._limit_total}, "
            f"offset: {self.offset}, page_size: {self._limit}"
        )
        return self._format_repr(params)

    async def get_next(self, **kwargs: Any) -> AsyncGenerator:
        if self.exhausted:
            return

        offset_limit = self._limit_total + self._offset_initial

        # Max number of records is less than or equals the
        # requested page size: set exhausted adjust the page size
        if offset_limit <= self.limit:
            self._limit = self._limit_total
            self.exhausted = True
        # Offset is greater or equals the offset limit: set exhausted
        # and adjust the final page size
        elif self.offset >= offset_limit:
            self.exhausted = True
            if self.offset == offset_limit:  # No need to fetch an empty page
                return

            # Adjust limit to get the last X records
            # This could be a fraction of a really large page
            self._limit = offset_limit - self._limit_total
            self.log.debug(
                f"{self._req_id}: Limit of {self.limit} records reached, setting exhausted"
            )

        response = await self.send(**kwargs)
        self._offset += self._limit

        if "next" not in response.links:
            self.exhausted = True
            self.log.debug(f"{self._req_id}: No more pages, setting exhausted")

        await response.load_document()
        yield response
