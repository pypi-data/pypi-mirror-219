from typing import Optional

from .client import BaseResource, BaseClient, ResourceCollection, PaginatorParams


class Client(BaseClient):
    def movie(self, movie_id):
        return Movie(self, f"/movie/{movie_id}")

    def quote(self, quote_id):
        return Quote(self, f"/quote/{quote_id}")

    def movies(
        self, sort: Optional[str] = None, page_size: int = 1000
    ) -> "ResourceCollection[Movie]":
        return self._collection(Movie, "movie", PaginatorParams(sort, page_size))

    def quotes(
        self, sort: Optional[str] = None, page_size: int = 1000
    ) -> "ResourceCollection[Quote]":
        return self._collection(Quote, "quote", PaginatorParams(sort, page_size))


class Resource(BaseResource):
    _client: Client


class Movie(Resource):
    @property
    def name(self) -> str:
        return self.raw_data["name"]

    @property
    def runtime_in_minutes(self) -> int:
        return self.raw_data["runtimeInMinutes"]

    @property
    def budget_in_millions(self) -> float:
        return self.raw_data["budgetInMillions"]

    @property
    def box_office_revenue_in_millions(self) -> float:
        return self.raw_data["boxOfficeRevenueInMillions"]

    @property
    def academy_awards_nominations(self) -> int:
        return self.raw_data["academyAwardNominations"]

    @property
    def academy_awards_wins(self) -> int:
        return self.raw_data["academyAwardWins"]

    @property
    def rotten_tomatoes_score(self) -> int:
        return self.raw_data["rottenTomatoesScore"]

    def quotes(self, sort: Optional[str] = None, page_size: int = 1000):
        return self._collection(Quote, "quote", PaginatorParams(sort, page_size))


class Quote(Resource):
    @property
    def dialog(self) -> str:
        return self.raw_data["dialog"]

    @property
    def movie_id(self) -> str:
        return self.raw_data["movie"]

    @property
    def character_id(self) -> str:
        return self.raw_data["character"]

    def movie(self) -> Movie:
        return self._client.movie(self.movie_id)
