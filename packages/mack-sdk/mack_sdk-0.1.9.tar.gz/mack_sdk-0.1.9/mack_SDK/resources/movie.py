import httpx

from mack_SDK.resources import models
from mack_SDK.tools.raise_for_status import raise_for_status


class Movie(object):
    """Movie resource class.

    This class is responsible for making requests to the /movie resource (endpoint)
    """

    http_client: httpx.Client

    def __init__(self, http_client: httpx.Client):
        """Initialize the class.

        Args:
            http_client : `httpx.Client` object
        """
        self.http_client = http_client

    def get_all_movies(
        self,
        limit: int = None,
        page: int = None,
        offset: int = None,
    ) -> models.MoviesModel:
        """Get all LOTR movies.

        Args:
            limit : Number of quotes to return
            page : Page number to return
            offset : Offset

        Returns:
            models.MoviesModel : List of all LOTR movies with pagination info

        Raises:
            HTTPStatusError : If status code is 4xx or 5xx # noqa: DAR402
        """
        params = {"limit": limit, "page": page, "offset": offset}  # noqa: WPS110
        res = self.http_client.request(method="GET", url="/movie", params=params)
        raise_for_status(res)
        return models.MoviesModel.parse_obj(res.json())

    def get_movie(self, item_id: str) -> models.MovieModel:
        """Get a single movie by ID.

        Args:
            item_id : ID of the movie to get

        Returns:
            models.MovieModel : LOTR movie object

        Raises:
            HTTPStatusError : If status code is 4xx or 5xx # noqa: DAR402
        """
        res = self.http_client.request(method="GET", url=f"/movie/{item_id}")
        raise_for_status(res)
        return models.MovieModel.parse_obj(res.json()["docs"][0])

    def get_quotes(
        self,
        item_id: str,
        limit: int = None,
        page: int = None,
        offset: int = None,
    ) -> models.QuotesModel:
        """Get quotes for a single movie.

        Args:
            item_id : ID of the movie to get quotes for
            limit : Number of quotes to return
            page : Page number to return
            offset : Offset

        Returns:
            models.QuotesModel : List of quotes for the movie with pagination info

        Raises:
            HTTPStatusError : If status code is 4xx or 5xx # noqa: DAR402
        """
        params = {"limit": limit, "page": page, "offset": offset}  # noqa: WPS110
        res = self.http_client.request(method="GET", url=f"/movie/{item_id}/quote", params=params)
        raise_for_status(res)
        return models.QuotesModel.parse_obj(res.json())
