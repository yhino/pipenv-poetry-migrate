from pathlib import Path

import tomlkit
from pipenv_poetry_migrate import __version__
from tomlkit import table


def test_version() -> None:
    with Path("pyproject.toml").open("r") as f:
        pyproject = tomlkit.loads(f.read())
    pyproject_tool = pyproject.get("tool", table(is_super_table=True))
    poetry = pyproject_tool.get("poetry", table())
    assert __version__ == poetry.get("version")
