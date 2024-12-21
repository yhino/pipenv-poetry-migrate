#!/usr/bin/env bash

set -x

poetry run ruff check --fix .
poetry run ruff format .
