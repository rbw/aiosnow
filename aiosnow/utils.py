from math import floor, log as Log, pow
from typing import Tuple
from yarl import URL


def get_url(address: str, use_ssl: bool) -> str:
    """
    get_url returns the base url for a serviceNow request
    :param address: the host for the request (Ex: CompanyName.service-now.com)
    :param use_ssl: describes whether to use https or http
    :return: returns the built URL (Ex: http://CompanyName.service-now.com)
    """
    snow_url = URL.build(
        schema=use_ssl and "https" or "http",
        host=address
    )
    return snow_url.human_repr()


def convert_size(size_bytes: int) -> Tuple[float, str]:
    if size_bytes == 0:
        return 0, "B"

    units = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    log = int(floor(Log(size_bytes, 1024)))
    power = pow(1024, log)
    size = round(size_bytes / power, 2)
    return size, units[log]
