#!/usr/bin/env bash

set -e
set -x

export PYTHONPATH=.
poetry run pytest -vv --cov=pipenv_poetry_migrate --cov-report=term tests ${@}
