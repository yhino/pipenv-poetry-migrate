import tomlkit

from pipenv_poetry_migrate import __version__


def test_version():
    with open("pyproject.toml", "r") as f:
        p = tomlkit.loads(f.read())
    assert __version__ == p["tool"]["poetry"]["version"]
