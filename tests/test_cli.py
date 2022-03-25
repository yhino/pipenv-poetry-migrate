from pathlib import Path

from typer.testing import CliRunner

from pipenv_poetry_migrate import __version__
from pipenv_poetry_migrate.cli import app

runner = CliRunner(mix_stderr=False)


def test_main(pipfile: Path, pyproject_toml: Path):
    argv = ["-f", str(pipfile), "-t", str(pyproject_toml), "-n"]
    result = runner.invoke(app, argv)

    assert result.exit_code == 0
    assert result.stdout != ""


def test_main_show_version():
    argv = ["-v"]
    result = runner.invoke(app, argv)

    assert result.exit_code == 0
    assert __version__ in result.stdout
    assert result.stderr == ""


def test_main_raise_pipfile_not_found_error(pyproject_toml: Path):
    argv = ["-f", "not_found.toml", "-t", str(pyproject_toml), "-n"]
    result = runner.invoke(app, argv)

    assert result.exit_code == 1
    assert result.stdout == ""
    assert "Pipfile 'not_found.toml' not found" in result.stderr


def test_main_raise_pyproject_toml_not_found_error(pipfile: Path):
    argv = ["-f", str(pipfile), "-t", "not_found.toml", "-n"]
    result = runner.invoke(app, argv)

    assert result.exit_code == 1
    assert result.stdout == ""
    assert "Please run `poetry init` first" in result.stderr
