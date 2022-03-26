from pathlib import Path

from pipenv_poetry_migrate.loader import load_toml
from pipenv_poetry_migrate.migrate import PipenvPoetryMigration


def test_migrate(
    pipenv_poetry_migration: PipenvPoetryMigration, expect_pyproject_toml: Path
):
    pipenv_poetry_migration.migrate()

    actual = load_toml(pipenv_poetry_migration.pyproject_toml())
    expect = load_toml(expect_pyproject_toml)
    assert actual == expect


def test_migrate_with_use_group_notation(
    pipenv_poetry_migration_with_use_group_notation: PipenvPoetryMigration,
    expect_pyproject_toml_with_use_group_notation: Path,
):
    pipenv_poetry_migration_with_use_group_notation.migrate()

    actual = load_toml(pipenv_poetry_migration_with_use_group_notation.pyproject_toml())
    expect = load_toml(expect_pyproject_toml_with_use_group_notation)
    assert actual == expect
