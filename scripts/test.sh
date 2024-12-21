#!/usr/bin/env bash

set -x

export PYTHONPATH=.
poetry run pytest -vv --cov=pipenv_poetry_migrate --cov-report=term tests ${@}
