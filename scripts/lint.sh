#!/usr/bin/env bash

set -ue
set -x

poetry run mypy .
poetry run ruff check .
poetry run ruff format --check --diff .
