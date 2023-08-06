from functools import reduce


def join_urls(*urls: str):
    """
    Join the given strings together, inserting / in between where necessary
    """
    return reduce(
        lambda url1, url2: f'{url1.rstrip("/")}/{url2.lstrip("/")}', urls
    ).rstrip("/")
