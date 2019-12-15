class SnowstormException(Exception):
    pass


class StreamExhausted(SnowstormException):
    pass


class NoSchemaFields(SnowstormException):
    pass


class PayloadValidationError(SnowstormException):
    pass
