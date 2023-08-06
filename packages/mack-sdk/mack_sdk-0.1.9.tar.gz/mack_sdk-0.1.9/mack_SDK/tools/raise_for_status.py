import time
from math import ceil

import httpx


def raise_for_status(res: httpx.Response) -> None:
    """Exception helper `for httpx.Response`.

    This helper raises an exception if the response status code is 4xx or 5xx
    Additionally sets custom error message for 429 status code with time to retry in (seconds)
    More elegant way would be subclassing the `httpx.Client()` and adding custom message,
    however for the sake of time we use this helper

    Args:
        res : `httpx.Response` object

    Raises:
        HTTPStatusError : If status code is 4xx or 5xx
    """
    if res.status_code == 429:  # noqa: WPS432
        retry_in = int(res.headers["X-RateLimit-Reset"]) - ceil(time.time())
        raise httpx.HTTPStatusError(
            f"Rate limit exceeded, retry after {retry_in}s",
            request=res.request,
            response=res,
        )
    res.raise_for_status()
