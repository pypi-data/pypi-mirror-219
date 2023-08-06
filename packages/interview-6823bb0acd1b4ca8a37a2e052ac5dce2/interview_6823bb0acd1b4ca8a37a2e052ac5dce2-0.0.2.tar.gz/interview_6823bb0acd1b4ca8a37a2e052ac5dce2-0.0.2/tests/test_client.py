import functools
import itertools
import os
import unittest.mock
from pathlib import Path

import responses
import responses._recorder

from lotr_sdk import Client

client = Client(os.environ.get("THE_ONE_API_KEY", ""))

RESPONSES_MODE = os.environ.get("RECORD_RESPONSES_MODE", "replay")


def record_responses(func):
    path = Path(__file__).parent / "recorded_responses" / f"{func.__name__}.yml"
    if RESPONSES_MODE == "replay":
        func = responses.activate(func)
    elif RESPONSES_MODE == "record":
        func = responses._recorder.record(file_path=path)(func)

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if RESPONSES_MODE == "replay":
            responses._add_from_file(file_path=path)
        return func(*args, **kwargs)

    return wrapper


def check_movie(movie):
    assert movie.raw_data == {
        "_id": movie.id,
        "name": movie.name,
        "runtimeInMinutes": movie.runtime_in_minutes,
        "budgetInMillions": movie.budget_in_millions,
        "boxOfficeRevenueInMillions": movie.box_office_revenue_in_millions,
        "academyAwardNominations": movie.academy_awards_nominations,
        "academyAwardWins": movie.academy_awards_wins,
        "rottenTomatoesScore": movie.rotten_tomatoes_score,
    }


def check_quote(quote):
    assert quote.raw_data == {
        "_id": quote.id,
        "id": quote.id,
        "dialog": quote.dialog,
        "movie": quote.movie_id,
        "character": quote.character_id,
    }


def check_movies_collection(collection):
    size = len(collection)
    lst = list(collection)
    assert len(lst) == len(set(lst)) == size == 8
    assert list(collection) == []

    for movie in lst:
        check_movie(movie)

    if collection._paginator.params.sort == "name:asc":
        assert lst == sorted(lst, key=lambda m: m.name)
    elif collection._paginator.params.sort == "name:desc":
        assert lst == sorted(lst, key=lambda m: m.name, reverse=True)
    return lst


def check_quotes_collection(collection):
    size = len(collection)
    max_items = 5
    lst = list(itertools.islice(collection, max_items))
    assert len(lst) == len(set(lst)) == min(size, max_items)
    for quote in lst:
        check_quote(quote)
    return lst


@record_responses
def test_movies_collection():
    check_movies_collection(client.movies(sort="name:asc"))
    check_movies_collection(client.movies(sort="name:desc", page_size=3))


@record_responses
def test_quotes_collection():
    check_quotes_collection(client.quotes(page_size=3))


@record_responses
def test_movie_by_id():
    movie_id = "5cd95395de30eff6ebccde5c"
    movie = client.movie(movie_id)
    check_movie(movie)
    assert movie.raw_data == {
        "_id": movie_id,
        "name": "The Fellowship of the Ring",
        "runtimeInMinutes": 178,
        "budgetInMillions": 93,
        "boxOfficeRevenueInMillions": 871.5,
        "academyAwardNominations": 13,
        "academyAwardWins": 4,
        "rottenTomatoesScore": 91,
    }
    quotes = check_quotes_collection(movie.quotes(page_size=3))
    for quote in quotes:
        assert quote.movie() == movie


@record_responses
def test_quote_by_id():
    quote_id = "5cd96e05de30eff6ebccf0d0"
    quote = client.quote(quote_id)
    check_quote(quote)
    assert quote.raw_data == {
        "_id": quote_id,
        "id": quote_id,
        "character": "5cd99d4bde30eff6ebccfea0",
        "dialog": "Fool of a Took! Throw yourself in next time, and rid us of your "
        "stupidity!",
        "movie": "5cd95395de30eff6ebccde5c",
    }


@record_responses
def test_close():
    temp_client = Client("")
    # requests.Session.close surprisingly has no easily testable effect
    temp_client.session.close = unittest.mock.Mock()  # type: ignore
    with temp_client:
        assert temp_client.session.get("https://httpbin.org/get").ok
    temp_client.session.close.assert_called_once()
