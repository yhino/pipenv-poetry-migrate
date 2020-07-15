from pathlib import Path

import pytest
from tomlkit.exceptions import ParseError
from tomlkit.toml_document import TOMLDocument

from pipenv_poetry_migrate.migrate import PipenvPoetryMigration, load_toml


def test_load_toml(pyproject_toml: Path):
    toml = load_toml(str(pyproject_toml))
    assert isinstance(toml, TOMLDocument)
    assert toml["tool"]["poetry"]["name"] == "pipenv-poetry-migrate-tests"


def test_load_toml_file_not_found():
    with pytest.raises(FileNotFoundError):
        load_toml("not_found.toml")


def test_load_toml_parse_error():
    with pytest.raises(ParseError):
        load_toml("tests/toml/broken.toml")


def test_migrate(
    pipenv_poetry_migration: PipenvPoetryMigration, expect_pyproject_toml: Path
):
    pipenv_poetry_migration.migrate()

    actual = load_toml(pipenv_poetry_migration.pyproject_toml())
    expect = load_toml(str(expect_pyproject_toml))
    assert actual == expect
