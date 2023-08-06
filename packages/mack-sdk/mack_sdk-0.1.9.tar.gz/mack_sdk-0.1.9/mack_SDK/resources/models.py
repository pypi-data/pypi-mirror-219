from pydantic import BaseModel
from pydantic import Field


class PageMeta(BaseModel):
    """Page meta data.

    Represents the meta data of a page of results.
    offset, page, pages may be None in various pagination combinations
    """

    total: int
    limit: int
    offset: int | None
    page: int | None
    pages: int | None


class MovieModel(BaseModel):
    """Single movie model."""

    id: str = Field(alias="_id")
    name: str
    runtime_in_minutes: int = Field(alias="runtimeInMinutes")
    budget_in_millions: int = Field(alias="budgetInMillions")
    box_office_revenue_in_millions: int = Field(alias="boxOfficeRevenueInMillions")
    academy_award_nominations: int = Field(alias="academyAwardNominations")
    academy_award_wins: int = Field(alias="academyAwardWins")
    rotten_tomatoes_score: int = Field(alias="rottenTomatoesScore")


class MoviesModel(PageMeta):
    """Multiple movies model.

    Contains a list (page) of movies and page meta data.
    """

    docs: list[MovieModel]


class QuoteModel(BaseModel):
    """Single movie model."""

    id: str = Field(alias="_id")
    dialog: str
    movie: str
    character: str


class QuotesModel(PageMeta):
    """Multiple quotes model.

    Contains a list (page) of movies and page meta data.
    """

    docs: list[QuoteModel]
