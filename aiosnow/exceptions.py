class AiosnowException(Exception):
    pass


class ConfigurationError(AiosnowException):
    """Configuration error"""


class StreamExhausted(AiosnowException):
    """Signals there are no further items produced by the iterator"""


class NoAuthenticationMethod(AiosnowException):
    """No authentication method was provided"""


class UnexpectedContentType(AiosnowException):
    """Unexpected content type from server"""


class ClientConnectionError(AiosnowException):
    """Raised when there was a problem connecting to the server"""


class SerializationError(AiosnowException):
    """Raised when there was an issue with serialization"""


class DeserializationError(AiosnowException):
    """Raised when there was an issue with deserialization"""


class RequestError(AiosnowException):
    """The application returned an error in the response"""

    def __init__(self, message: str, status: int):
        self.message = message
        self.status = status


class ServerError(RequestError):
    """The server returned an error in the response"""


class UnexpectedResponseContent(RequestError):
    """Unexpected content in response from server"""


class UnexpectedPayloadType(AiosnowException):
    """Raised when the request payload was of an unexpected type"""


class PayloadValidationError(AiosnowException):
    """Local payload validation against a Resource Schema failed"""


class IncompatiblePayloadField(AiosnowException):
    """An incompatible field was found in the payload"""


class UnknownPayloadField(AiosnowException):
    """A field unknown to the schema was found in the payload"""


class IncompatibleSession(AiosnowException):
    """Raised if a custom session object passed to aiosnow.Client is not of aiosnow.Session type"""


class UnexpectedValue(AiosnowException):
    """Typically raised when a method receives unexpected input"""


class SchemaError(AiosnowException):
    """Generic exception raised on schema issues, e.g. integrity errors"""


class SelectError(AiosnowException):
    """Raised on query builder issues"""


class InvalidContentMethod(AiosnowException):
    """Raised if the response content was incorrectly accessed"""


class InvalidFieldName(AiosnowException):
    """Usually raised if an attempt is made to override a base member with a Field"""


class NoSchemaFields(AiosnowException):
    """The schema lacks definition"""


class TooManyItems(AiosnowException):
    """The request yielded too many results"""


class NoItems(AiosnowException):
    """The request yielded no results"""


class DeleteError(AiosnowException):
    """Raised if there was an error deleting a record"""
