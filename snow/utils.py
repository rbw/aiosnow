def get_url(address, use_ssl):
    url_scheme = use_ssl and "https://" or "http://"
    return url_scheme + str(address)
