import math
from typing import Tuple


def convert_size(size_bytes: int) -> Tuple[float, str]:
    if size_bytes == 0:
        return 0, "B"

    units = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    log = int(math.floor(math.log(size_bytes, 1024)))
    power = math.pow(1024, log)
    size = round(size_bytes / power, 2)
    return size, units[log]
