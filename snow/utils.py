def get_url(address: str, use_ssl: bool) -> str:
    url_scheme = use_ssl and "https://" or "http://"
    return url_scheme + str(address)
