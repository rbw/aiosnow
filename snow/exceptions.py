class SnowException(Exception):
    pass


class ConfigurationException(SnowException):
    """Configuration error"""


class StreamExhausted(SnowException):
    """Signals there are no further items produced by the iterator"""


class NoAuthenticationMethod(SnowException):
    """No authentication method was provided"""


class UnexpectedContentType(SnowException):
    """Unexpected content type from server"""


class ClientConnectionError(SnowException):
    """Raised when there was a problem connecting to the server"""


class RequestError(SnowException):
    """The application returned an error in the response"""

    def __init__(self, message: str, status: int):
        self.message = message
        self.status = status


class ServerError(RequestError):
    """The server returned an error in the response"""


class UnexpectedResponseContent(RequestError):
    """Unexpected content in response from server"""


class UnexpectedPayloadType(SnowException):
    """Raised when the request payload was of an unexpected type"""


class PayloadValidationError(SnowException):
    """Local payload validation against a Resource Schema failed"""


class IncompatiblePayloadField(SnowException):
    """An incompatible field was found in the payload"""


class UnknownPayloadField(SnowException):
    """A field unknown to the schema was found in the payload"""


class IncompatibleSession(SnowException):
    """Raised if a custom session object passed to snow.Application is not of snow.Session type"""


class UnexpectedValue(SnowException):
    """Typically raised when a Snow method receives unexpected input"""


class SchemaError(SnowException):
    """Generic exception raised on schema issues, e.g. integrity errors"""


class SelectError(SnowException):
    """Raised on query builder issues"""


class InvalidContentMethod(SnowException):
    """Raised if the response content was incorrectly accessed"""


class UnexpectedModelSchema(SnowException):
    """Raised if an unexpected Schema was passed to Model"""


class NoSchemaFields(SnowException):
    """The schema lacks definition"""


class TooManyItems(SnowException):
    """The request yielded too many results"""


class NoItems(SnowException):
    """The request yielded no results"""
