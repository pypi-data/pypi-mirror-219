from dataclasses import dataclass
from typing import TypeVar, Iterable, Iterator, Optional, Type, Dict, Union

from requests import Session

from .utils import join_urls


@dataclass
class PaginatorParams:
    sort: Optional[str]
    page_size: int


T = TypeVar("T", bound="BaseResource")


class BaseClient:
    def __init__(
        self,
        api_key: str,
        *,
        root="https://the-one-api.dev/v2",
    ):
        self.root = root
        self.session = Session()
        self.session.headers.update(
            {
                "Authorization": f"Bearer {api_key}",
            }
        )

    def _get(self, path: str, params: Optional[dict] = None):
        url = join_urls(self.root, path)
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def close(self):
        self.session.close()

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()

    def _collection(
        self,
        resource_type: Type[T],
        path: str,
        params: PaginatorParams,
    ) -> "ResourceCollection[T]":
        return ResourceCollection(
            resource_type,
            Paginator(
                client=self,
                path=path,
                params=params,
            ),
        )


class Paginator(Iterable[dict]):
    def __init__(
        self,
        *,
        client: BaseClient,
        path: str,
        params: PaginatorParams,
    ):
        self.client = client
        self.path = path
        self.params = params
        self.page_num = 1
        self.current_response = self._get()

        def pages():
            yield self.current_response
            while True:
                if self.page_num >= self.current_response["pages"]:
                    break
                self.page_num += 1
                self.current_response = self._get()
                yield self.current_response

        self.pages = pages()

        def docs():
            for page in self.pages:
                yield from page["docs"]

        # Initialize the generator once to ensure that repeated calls to __iter__
        # don't mess with iterator state.
        # For example, looping fully exhausts the iterator so that subsequent
        # iteration yields nothing rather than making more network requests.
        # In general, looping a second time should always continue from the exact item
        # where the previous loop stopped.
        self._docs = docs()

    def __iter__(self) -> Iterator[dict]:
        return self._docs

    def _get(self) -> dict:
        params: Dict[str, Union[int, str]] = {
            "limit": self.params.page_size,
            "page": self.page_num,
        }
        if self.params.sort is not None:
            params["sort"] = self.params.sort
        return self.client._get(self.path, params=params)


class ResourceCollection(Iterable[T]):
    def __init__(self, resource_type: Type[T], paginator: Paginator):
        self._paginator = paginator
        self._resource_type = resource_type

    def __iter__(self) -> Iterator[T]:
        for raw_data in self._paginator:
            yield self._resource_type(
                self._paginator.client,
                join_urls(self._paginator.path, raw_data["_id"]),
                raw_data,
            )

    def __len__(self):
        return self._paginator.current_response["total"]


class BaseResource:
    def __init__(
        self,
        client: BaseClient,
        path: str,
        raw_data: Optional[dict] = None,
    ):
        self._client = client
        self._path = path
        if raw_data is None:
            [raw_data] = self._client._get(self._path)["docs"]
        assert raw_data is not None
        self.raw_data: dict = raw_data

    @property
    def id(self) -> str:
        return self.raw_data["_id"]

    def __eq__(self, other) -> bool:
        return type(self) == type(other) and self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)

    def _collection(
        self,
        resource_type: Type[T],
        subpath: str,
        params: PaginatorParams,
    ) -> ResourceCollection[T]:
        return self._client._collection(
            resource_type,
            join_urls(self._path, subpath),
            params,
        )
