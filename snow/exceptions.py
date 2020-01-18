class SnowException(Exception):
    pass


class StreamExhausted(SnowException):
    pass


class PayloadValidationError(SnowException):
    pass


class UnexpectedContentType(SnowException):
    pass


class ErrorResponse(SnowException):
    pass


class UnexpectedSchema(SnowException):
    pass


class UnexpectedValue(SnowException):
    pass


class SchemaError(SnowException):
    pass


class SelectError(SnowException):
    pass


class NoLocationField(SnowException):
    pass


class NoSchemaFields(SnowException):
    pass


class EmptyQuery(SnowException):
    pass


class TooManyResults(SnowException):
    pass


class NoResult(SnowException):
    pass
