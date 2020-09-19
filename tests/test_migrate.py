from pathlib import Path

from pipenv_poetry_migrate.loader import load_toml
from pipenv_poetry_migrate.migrate import PipenvPoetryMigration


def test_migrate(
    pipenv_poetry_migration: PipenvPoetryMigration, expect_pyproject_toml: Path
):
    pipenv_poetry_migration.migrate()

    actual = load_toml(pipenv_poetry_migration.pyproject_toml())
    expect = load_toml(str(expect_pyproject_toml))
    assert actual == expect
