from pathlib import Path

import pytest

from pipenv_poetry_migrate.migrate import PipenvPoetryMigration


@pytest.fixture
def pipfile() -> Path:
    return Path("tests/toml/Pipfile")


@pytest.fixture
def pyproject_toml() -> Path:
    return Path("tests/toml/pyproject.toml")


@pytest.fixture
def expect_pyproject_toml() -> Path:
    return Path("tests/toml/expect_pyproject.toml")


@pytest.fixture
def expect_pyproject_toml_with_use_group_notation() -> Path:
    return Path("tests/toml/expect_pyproject_with_use_group_notation.toml")


@pytest.fixture
def pipenv_poetry_migration(
    tmp_path: Path, pipfile: Path, pyproject_toml: Path
) -> PipenvPoetryMigration:
    replica_pyproject_toml = tmp_path / "pyproject.toml"
    replica_pyproject_toml.write_bytes(pyproject_toml.read_bytes())
    return PipenvPoetryMigration(str(pipfile), str(replica_pyproject_toml))


@pytest.fixture
def pipenv_poetry_migration_with_use_group_notation(
    tmp_path: Path, pipfile: Path, pyproject_toml: Path
) -> PipenvPoetryMigration:
    replica_pyproject_toml = tmp_path / "pyproject.toml"
    replica_pyproject_toml.write_bytes(pyproject_toml.read_bytes())
    return PipenvPoetryMigration(
        str(pipfile), str(replica_pyproject_toml), use_group_notation=True
    )
