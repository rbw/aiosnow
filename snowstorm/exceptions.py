class SnowstormException(Exception):
    pass


class StreamExhausted(SnowstormException):
    pass


class PayloadValidationError(SnowstormException):
    pass


class UnexpectedContentType(SnowstormException):
    pass


class ErrorResponse(SnowstormException):
    pass


class UnexpectedSchema(SnowstormException):
    pass


class UnexpectedValue(SnowstormException):
    pass


class SelectError(SnowstormException):
    pass


class NoLocationField(SnowstormException):
    pass


class NoSchemaFields(SnowstormException):
    pass


class EmptyQuery(SnowstormException):
    pass
