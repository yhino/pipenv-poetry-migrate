from pathlib import Path

import pytest


@pytest.fixture
def pipfile() -> Path:
    return Path("tests/toml/Pipfile")


@pytest.fixture
def pyproject_toml() -> Path:
    return Path("tests/toml/pyproject.toml")


@pytest.fixture
def poetry12_pyproject_toml() -> Path:
    return Path("tests/toml/poetry12_pyproject.toml")


@pytest.fixture
def expect_pyproject_toml_with_default_option() -> Path:
    return Path("tests/toml/expect_pyproject_with_default_option.toml")


@pytest.fixture
def expect_pyproject_toml_with_no_use_group_notation() -> Path:
    return Path("tests/toml/expect_pyproject_with_no_use_group_notation.toml")


@pytest.fixture
def expect_pyproject_toml_with_re_migrate() -> Path:
    return Path("tests/toml/expect_pyproject_with_re_migrate.toml")
