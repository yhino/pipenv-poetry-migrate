#!/usr/bin/env bash

set -ue
set -x

rm -rf build dist .eggs *.egg-info
rm -rf .coverage coverage.xml htmlcov report.xml .tox
find . -type d -name '.ruff_cache' -exec rm -rf {} +
find . -type d -name '.mypy_cache' -exec rm -rf {} +
find . -type d -name '__pycache__' -exec rm -rf {} +
find . -type d -name '*pytest_cache*' -exec rm -rf {} +
find . -type f -name '*.py[co]' -exec rm -rf {} +
