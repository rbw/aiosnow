class SnowstormException(Exception):
    pass


class StreamExhausted(SnowstormException):
    pass


class NoSchemaFields(SnowstormException):
    pass


class PayloadValidationError(SnowstormException):
    pass


class UnexpectedContentType(SnowstormException):
    pass


class ErrorResponse(SnowstormException):
    pass


class QueryTypeError(SnowstormException):
    pass
