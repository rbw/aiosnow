import aiohttp

from urllib.parse import urljoin, urlencode
import marshmallow

from snowstorm.selector import Selector
from snowstorm.exceptions import NoSchemaFields, PayloadValidationError

from .schema import Schema, SchemaOpts, String
from .query import QueryBuilder


class Resource:
    connection = None

    def __init__(self, schema_cls, config):
        self.config = config
        self.schema_cls = schema_cls
        self.fields = schema_cls._declared_fields
        if not self.fields:
            raise NoSchemaFields(f"Schema {self.schema_cls} lacks fields definitions")

        self.url_base = urljoin(self.config["base_url"], schema_cls.__location__)

    async def __aenter__(self):
        config = self.config
        self.connection = aiohttp.ClientSession(
            auth=aiohttp.helpers.BasicAuth(config["username"], config["password"]),
        )

        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.connection.close()

    def get_url(self, method="GET"):
        params = {}

        if method == "GET":
            params["sysparm_fields"] = ",".join(self.fields)

        return f"{self.url_base}{'?' + urlencode(params) if params else ''}"

    def build_query(self, query):
        return QueryBuilder(query)

    def select(self, query) -> Selector:
        return Selector(self, query)

    def select_raw(self, query) -> Selector:
        return Selector(self, query)

    async def create(self, **kwargs):
        try:
            payload = self.schema_cls(unknown=marshmallow.RAISE).load(kwargs)
        except marshmallow.exceptions.ValidationError as e:
            raise PayloadValidationError(e)

        print(payload)

        return
