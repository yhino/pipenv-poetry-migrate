from pathlib import Path
from typing import Any, Callable

import pytest
from pipenv_poetry_migrate.loader import load_toml
from pipenv_poetry_migrate.migrate import PipenvPoetryMigration


@pytest.fixture()
def load_fixture(request: pytest.FixtureRequest) -> Callable[[str], Any]:
    def _load_fixture(fixture_name: str) -> Any:
        return request.getfixturevalue(fixture_name)

    return _load_fixture


@pytest.mark.parametrize(
    ("pipfile_", "pyproject_toml_", "expect_pyproject_toml_"),
    [
        ("pipfile", "pyproject_toml", "expect_pyproject_toml"),
        ("pipfile", "poetry12_pyproject_toml", "expect_pyproject_toml"),
    ],
)
def test_migrate(
    pipfile_: str,
    pyproject_toml_: str,
    expect_pyproject_toml_: str,
    tmp_path: Path,
    load_fixture: Callable[[str], Any],
) -> None:
    replica_pyproject_toml = tmp_path.joinpath("pyproject")
    replica_pyproject_toml.write_bytes(load_fixture(pyproject_toml_).read_bytes())

    pipenv_poetry_migrate = PipenvPoetryMigration(
        load_fixture(pipfile_),
        replica_pyproject_toml,
    )
    pipenv_poetry_migrate.migrate()

    actual = load_toml(pipenv_poetry_migrate.pyproject_toml())
    expect = load_toml(load_fixture(expect_pyproject_toml_))
    assert actual == expect


@pytest.mark.parametrize(
    ("pipfile_", "pyproject_toml_", "expect_pyproject_toml_"),
    [
        (
            "pipfile",
            "pyproject_toml",
            "expect_pyproject_toml_with_use_group_notation",
        ),
        (
            "pipfile",
            "poetry12_pyproject_toml",
            "expect_pyproject_toml_with_use_group_notation",
        ),
    ],
)
def test_migrate_with_use_group_notation(
    pipfile_: str,
    pyproject_toml_: str,
    expect_pyproject_toml_: str,
    tmp_path: Path,
    load_fixture: Callable[[str], Any],
) -> None:
    replica_pyproject_toml = tmp_path.joinpath("pyproject")
    replica_pyproject_toml.write_bytes(load_fixture(pyproject_toml_).read_bytes())

    pipenv_poetry_migrate = PipenvPoetryMigration(
        load_fixture(pipfile_),
        replica_pyproject_toml,
        use_group_notation=True,
    )
    pipenv_poetry_migrate.migrate()

    actual = load_toml(pipenv_poetry_migrate.pyproject_toml())
    expect = load_toml(load_fixture(expect_pyproject_toml_))
    assert actual == expect
