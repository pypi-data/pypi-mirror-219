# `client.py`

Core implementation of the SDK without reference to specific resources/endpoints. It should be possible to copy this code to a different project with a similarly shaped API.

## `BaseClient`

Manages the HTTP session (with authentication), makes network requests, and parses responses. Other objects generally hold a reference to this object.

This would be the place to add things like retrying, error handling, caching, alternative transports, etc.

## `Paginator`

Manages paginating through items in a 'collection' endpoint, storing various bits of state, making requests (via the client) and yielding items as raw dictionaries. This allows bundling various internal attributes into a single object so that `ResourceCollection` only needs a single `_paginator` attribute which the curious can inspect.

## `ResourceCollection`

Wraps `Paginator` in the higher level interface described in the README. Iterating yields `BaseResource` objects of a specific type indicated by a generic type parameter. Also supports efficient `len()`.

## `BaseResource`

Base class for nice model objects wrapping the raw dictionaries returned by the API.

## `PaginatorParams`

Simple dataclass for bundling parameters to the `Paginator` constructor and other internal code leading there, rather than copying `sort=sort, page_size=page_size` everywhere along with similar future parameters.

External methods should provide keyword arguments for all parameters to make life easy for the user, then immediately put them into a `PaginatorParams` object to pass to internal code.

# `resources.py`

Extends the classes in `client.py` with the specific attributes and methods corresponding to the API endpoints. Implementing additional endpoints would all be done here. You should find it easy to imagine how to follow the patterns in the existing code.

## `Client`

Entry point for the SDK. Subclass of `client.BaseClient` with a method for each endpoint.

## `Resource`

Subclass of `client.BaseResource` that just hints at the correct type of `_client` so that actual resources can use methods of `Client` and type checkers are happy. Base class for all actual resource classes.

## `Movie` and `Quote`

Subclasses of `Resource`, the objects that the user interacts with representing individual data items.

Should have a snake-cased, type-hinted `@property` for each key in the raw data.

`Client` should have a method for each resource type to get a `ResourceCollection` of that type and another to get a single `Resource` of that type by ID.

When the API provides a 'subcollection' at a path relative to the endpoint for a single resource, the `Resource` should have a method for that subcollection. For example, `client.movie(movie_id).quotes()` returns a `ResourceCollection[Quote]` based on `/movies/{movie_id}/quotes`.

When the resource data contains an ID for another resource, the `Resource` should have:

- a property to return that ID, named `{resource}_id` (e.g. `movie_id`)
- a method to get that resource, named `{resource}()` (e.g. `movie()`)

# Config and scripts

Files that were mostly copied from other projects of mine for testing, packaging, etc:

- For PyPI packaging:
  - `setup.cfg`
  - `pyproject.toml`
  - `release.sh`
  - Among other things, these generate a `lotr_sdk/version.py` file containing `__version__ = '...'` which matches the version in PyPI and a git tag.
- `LICENSE.txt`
- `.gitignore`
- `.github/workflows/tests.yml`
- `.pre-commit-config.yaml` (particularly to ensure code is formatted with `black`)
- `tox.ini` for testing multiple python versions locally.
