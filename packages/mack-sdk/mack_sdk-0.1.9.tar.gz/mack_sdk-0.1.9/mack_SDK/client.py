import httpx

from mack_SDK.resources.movie import Movie
from mack_SDK.resources.quote import Quote
from mack_SDK.tools.settings import Settings


class Client(object):
    """Create LOTR API Client.

    This class is used to create a client for the LOTR API.
    API docs - https://the-one-api.dev/documentation.
    `BEARER_TOKEN` is required for the API to work ([get token](https://the-one-api.dev/sign-up)),
    it may be passed as an argument or set as an environment variable.
    Currently not supported: Filtering, Sorting, Pagination (needs to be implemented by the client
    user).

    Examples:
        ```python
        # Initialize a client
        import mack_SDK.client
        client = mack_SDK.client.Client(bearer_token="some_token")

        # Work with `/movies` resources:
        movie_client = client.create_resource_class("movie")
        movies = movie_client.get_all_movies(page=2)
        movie = movie_client.get_movie("5cd95395de30eff6ebccde5b")
        quotes = movie_client.get_quotes("5cd95395de30eff6ebccde5b", limit=10)

        # Work with `/quotes` resources:
        movie_client = client.create_resource_class("movie")
        quote_client = client.create_resource_class("quote")
        quotes = quote_client.get_all_quotes(limit=50, page=2)
        quote = quote_client.get_quote("5cd96e05de30eff6ebcce7ea")
    ```
    """

    http_client: httpx.Client

    def __init__(self, base_url: str = "https://the-one-api.dev/v2", bearer_token: str = None):
        """Create instance of the LOTR API client.

        Method instantiates the `httpx.Client()` and sets: `base_url`,
        `headers` (Content-Type, Authorization), SSL verification is on and can not be changed

        Args:
            base_url : Base URL for the `httpx.CLient()`
            bearer_token :  Bearer auth token. Get here -https://the-one-api.dev/sign-up
        """
        settings = Settings(BEARER_TOKEN=bearer_token)

        headers = httpx.Headers(
            {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {settings.BEARER_TOKEN}",
            },
        )
        self.http_client = httpx.Client(base_url=base_url, headers=headers, verify=True)

    def create_resource_class(self, resource_name: str) -> object:
        """Create an API resource (endpoint) class.

        Following endpoints are supported: `/movie`, `/movie/{id}`, `/movie/{id}/quote`, `/quote`,
        `/quote/{id}`

        Args:
            resource_name: Name of the resource (endpoint) class to create

        Returns:
            object: Resource class

        Raises:
            ValueError: If resource name is not supported
        """
        # We acknowledge that this is not the best way to do this, but to save time we use dirty way
        match resource_name.lower():
            case "movie":
                return Movie(self.http_client)
            case "quote":
                return Quote(self.http_client)
            case _:
                raise ValueError(f"Resource {resource_name} is not implemented")
