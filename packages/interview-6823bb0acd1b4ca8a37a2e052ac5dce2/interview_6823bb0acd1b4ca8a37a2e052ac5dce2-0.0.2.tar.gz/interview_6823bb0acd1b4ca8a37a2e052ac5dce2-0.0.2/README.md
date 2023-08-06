# Lord of the Rings SDK

Python client library for [The One API](https://the-one-api.dev/).

## Installation

```bash
pip install interview_6823bb0acd1b4ca8a37a2e052ac5dce2
```

## Usage

```python
import lotr_sdk

# Copy access token from https://the-one-api.dev/account (requires signup)
client = lotr_sdk.Client("YOUR_API_KEY")

for movie in client.movies():
    print(movie.name)
```

### Methods

```python
# Get all movies
client.movies()

# Get all quotes
client.quotes()

# Get one movie by ID
client.movie("ID")

# Get one quote by ID
client.quote("ID")

# Get all quotes of a movie
client.movie("MOVIE_ID").quotes()

# Get the movie of a quote
client.quote("QUOTE_ID").movie()
```

### Resources

Individual movies and quotes are instances of `Resource` and have the following in common:

- `resource.id`: a unique string identifier
- `resource.raw_data`: a dictionary of the raw JSON data returned by the API, with `camelCase` keys
- Support for equality and hashing based on `resource.id`

Each class also has `snake_case` attributes for each key in the data, e.g:

```python
assert movie.runtime_in_minutes == movie.raw_data["runtimeInMinutes"]
```

Note that `quote.movie()` makes a network request and returns a movie object, while `quote.movie_id` just retrieves the ID from the raw data. Similarly use `quote.character_id`, while `quote.character()` is not implemented yet.

### Collections

The `.movies()` and `.quotes()` methods (both on the client and on the resources) return a `ResourceCollection` object. This automatically makes an initial network request.

Iterating over a collection will automatically paginate through the results, making additional network requests as needed, and yielding resource objects. You cannot iterate over a collection more than once.

`len(collection)` will return the total number of results without needing to make additional network requests or iterate through the whole collection.

To control the order of objects returned by the API, use the `sort` parameter, e.g:

```python
client.movies(sort="runtimeInMinutes:asc")  # note the camelCase
movie.quotes(sort="dialog:desc")
```

By default, the API returns 1000 results per 'page'. You can change this with the `page_size` parameter which may improve overall performance.

## Development

### Setup

1. Clone the repo
2. Create a virtual environment: `python3 -m venv venv`
3. Activate the virtual environment: `source venv/bin/activate`
4. Install dependencies: `pip install -e '.[dev]'`
5. Install git hooks: `pre-commit install`

### Testing

Run `pytest` to run the tests.

By default, API requests are mocked using the `responses` library and data stored in `tests/recorded_responses`. To update the recorded response data, set the environment variables `RECORD_RESPONSES_MODE=record` and `THE_ONE_API_KEY=<your key>`. To not use `responses` at all, set `RECORD_RESPONSES_MODE=none`. Note that requests are limited by the API to 100 per 10 minutes.

To test multiple Python versions (3.7 to 3.11 are supported) install those versions (e.g. using [`pyenv`](https://github.com/pyenv/pyenv)) and then install and run [`tox`](https://tox.wiki).

### Releasing to PyPI

1. `pip install tox build twine`
2. `./release.sh <version>` e.g. `./release.sh 1.2.3`
