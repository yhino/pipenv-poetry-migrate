from pathlib import Path

from tomlkit import loads
from tomlkit.toml_document import TOMLDocument


class PipfileNotFoundError(FileNotFoundError):
    pass


class PyprojectTomlNotFoundError(FileNotFoundError):
    pass


def load_toml(filepath: Path) -> TOMLDocument:
    with filepath.open("r") as f:
        return loads(f.read())


def load_pipfile(filepath: Path) -> TOMLDocument:
    try:
        return load_toml(filepath)
    except FileNotFoundError as exc:
        raise PipfileNotFoundError from exc


def load_pyproject_toml(filepath: Path) -> TOMLDocument:
    try:
        return load_toml(filepath)
    except FileNotFoundError as exc:
        raise PyprojectTomlNotFoundError from exc
