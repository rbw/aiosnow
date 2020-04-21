class SnowException(Exception):
    pass


class ConfigurationException(SnowException):
    """Configuration error"""


class StreamExhausted(SnowException):
    """Signals there are no further items produced by the iterator"""


class PayloadValidationError(SnowException):
    """Local payload validation against a Resource Schema failed"""


class NoAuthenticationMethod(SnowException):
    """No authentication method was provided"""


class UnexpectedContentType(SnowException):
    """Unexpected content type from server"""


class ClientConnectionError(SnowException):
    """Raised when there was a problem connecting to the server"""


class ServerError(SnowException):
    """The server returned an error response"""

    def __init__(self, message, status):
        self.message = message
        self.status = status


class RequestError(ServerError):
    """The server application returned an error in the response"""


class IncompatiblePayloadField(SnowException):
    """An incompatible field was found in the payload"""


class UnknownPayloadField(SnowException):
    """A field unknown to the schema was found in the payload"""


class UnexpectedSchema(SnowException):
    """Schema not of snow.resource.schema.Schema type"""


class UnexpectedValue(SnowException):
    """Typically raised when a Snow method receives unexpected input"""


class SchemaError(SnowException):
    """Generic exception raised on schema issues, e.g. integrity errors"""


class SelectError(SnowException):
    """Raised on query builder issues"""


class NoSchemaFields(SnowException):
    """The schema lacks fields definitions"""


class TooManyItems(SnowException):
    """The request yielded too many results"""


class NoItems(SnowException):
    """The request yielded no results"""
