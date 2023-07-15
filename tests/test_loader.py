from pathlib import Path

import pytest
from tomlkit import table
from tomlkit.exceptions import ParseError
from tomlkit.toml_document import TOMLDocument

from pipenv_poetry_migrate.loader import (
    PipfileNotFoundError,
    PyprojectTomlNotFoundError,
    load_pipfile,
    load_pyproject_toml,
    load_toml,
)


def test_load_toml(pyproject_toml: Path) -> None:
    toml = load_toml(pyproject_toml)

    assert isinstance(toml, TOMLDocument)
    assert (
        toml.get("tool", table(is_super_table=True)).get("poetry", table()).get("name")
        == "pipenv-poetry-migrate-tests"
    )


def test_load_toml_file_not_found() -> None:
    with pytest.raises(FileNotFoundError):
        load_toml(Path("not_found.toml"))


def test_load_toml_parse_error() -> None:
    with pytest.raises(ParseError):
        load_toml(Path("tests/toml/broken.toml"))


def test_load_pipfile(pipfile: Path) -> None:
    toml = load_pipfile(pipfile)

    assert isinstance(toml, TOMLDocument)


def test_load_pipfile_fails_file_not_found() -> None:
    with pytest.raises(PipfileNotFoundError):
        load_pipfile(Path("not_found.toml"))


def test_load_pyproject_toml(pyproject_toml: Path) -> None:
    toml = load_pyproject_toml(pyproject_toml)

    assert isinstance(toml, TOMLDocument)


def test_load_pyproject_toml_fails_file_not_found() -> None:
    with pytest.raises(PyprojectTomlNotFoundError):
        load_pyproject_toml(Path("not_found.toml"))
