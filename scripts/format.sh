#!/usr/bin/env bash

set -ue
set -x

poetry run ruff check --fix .
poetry run ruff format .
