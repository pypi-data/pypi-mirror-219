# Overview
This is a Python SDK for the [The One API](https://the-one-api.dev/) (not fully implemented).

API Overview is [here](./docs/README.md).

Example usage may be found [here](./docs/client.md#Examples).

**Rate limit retry is not implemented, you may get 429 errors**

# Install
`pip install mack-sdk`

# Development
`pre-commit` hooks is heavily used for various linting and formatting tasks.
We rely on [poetry](https://python-poetry.org/) for dependency management.
`make` is used to spin-up local environment:
* `make development` to install all dependencies
* `make lint` to run linting
* `make test` to run all tests
* `make test TESTS=tests/unit/client_test.py` to run tests from a file
