import httpx

from mack_SDK.resources import models
from mack_SDK.tools.raise_for_status import raise_for_status


class Quote(object):
    """Quote resource class.

    This class is responsible for making requests to the /quote resource (endpoint)
    """

    http_client: httpx.Client

    def __init__(self, http_client: httpx.Client):
        """Initialize the class.

        Args:
            http_client : `httpx.Client` object
        """
        self.http_client = http_client

    def get_all_quotes(
        self,
        limit: int = 100,
        page: int = 1,
        offset: int = 0,
    ) -> models.QuotesModel:
        """Get all LOTR quotes.

        Args:
            limit : Number of quotes to return
            page : Page number to return
            offset : Offset

        Returns:
            models.QuotesModel : List of all LOTR quotes with pagination info

        Raises:
            HTTPStatusError : If status code is 4xx or 5xx # noqa: DAR402
        """
        params = {"limit": limit, "page": page, "offset": offset}  # noqa: WPS110
        res = self.http_client.request(method="GET", url="/quote", params=params)
        raise_for_status(res)
        return models.QuotesModel.parse_obj(res.json())

    def get_quote(self, item_id: str) -> models.QuoteModel:
        """Get a single quote by ID.

        Args:
            item_id : ID of the quote to get

        Returns:
            models.MovieModel : LOTR quote object

        Raises:
            HTTPStatusError : If status code is 4xx or 5xx # noqa: DAR402
        """
        res = self.http_client.request(method="GET", url=f"/quote/{item_id}")
        raise_for_status(res)
        return models.QuoteModel.parse_obj(res.json()["docs"][0])
