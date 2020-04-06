def serialize_list(values):
    values = map(str, values)
    return ",".join(values)
