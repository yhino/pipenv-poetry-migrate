from pathlib import Path

import pytest


@pytest.fixture()
def pipfile() -> Path:
    return Path("tests/toml/Pipfile")


@pytest.fixture()
def pyproject_toml() -> Path:
    return Path("tests/toml/pyproject.toml")


@pytest.fixture()
def poetry12_pyproject_toml() -> Path:
    return Path("tests/toml/poetry12_pyproject.toml")


@pytest.fixture()
def expect_pyproject_toml() -> Path:
    return Path("tests/toml/expect_pyproject.toml")


@pytest.fixture()
def expect_pyproject_toml_with_use_group_notation() -> Path:
    return Path("tests/toml/expect_pyproject_with_use_group_notation.toml")
