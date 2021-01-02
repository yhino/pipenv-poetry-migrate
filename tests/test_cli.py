import sys
from pathlib import Path

import pytest

from pipenv_poetry_migrate import __version__
from pipenv_poetry_migrate.cli import main


def test_main(monkeypatch, capfd, pipfile: Path, pyproject_toml: Path):
    with monkeypatch.context() as m:
        argv = ["-f", str(pipfile), "-t", str(pyproject_toml), "-n"]
        m.setattr(sys, "argv", [""] + argv)
        main()

        captured = capfd.readouterr()
        assert captured.out != ""
        assert captured.err == ""


def test_main_show_version(monkeypatch, capfd):
    with monkeypatch.context() as m:
        with pytest.raises(SystemExit) as e:
            m.setattr(sys, "argv", ["", "-v"])
            main()

            assert e.value.code == 0
        captured = capfd.readouterr()
        assert __version__ in captured.out
        assert captured.err == ""


def test_main_raise_pipfile_not_found_error(monkeypatch, capfd, pyproject_toml: Path):
    with monkeypatch.context() as m:
        with pytest.raises(SystemExit) as e:
            argv = ["-f", "not_found.toml", "-t", str(pyproject_toml), "-n"]
            m.setattr(sys, "argv", [""] + argv)
            main()

            assert e.value.code == 1
        captured = capfd.readouterr()
        assert captured.out == ""
        assert "Pipfile 'not_found.toml' not found" in captured.err


def test_main_raise_pyproject_toml_not_found_error(monkeypatch, capfd, pipfile: Path):
    with monkeypatch.context() as m:
        with pytest.raises(SystemExit) as e:
            argv = ["-f", str(pipfile), "-t", "not_found.toml", "-n"]
            m.setattr(sys, "argv", [""] + argv)
            main()

            assert e.value.code == 1
        captured = capfd.readouterr()
        assert captured.out == ""
        assert "Please run `poetry init` first" in captured.err
