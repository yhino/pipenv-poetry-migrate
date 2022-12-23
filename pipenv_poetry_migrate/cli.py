from pathlib import Path
from typing import Optional

import typer

from pipenv_poetry_migrate import __version__
from pipenv_poetry_migrate.loader import (
    PipfileNotFoundError,
    PyprojectTomlNotFoundError,
)
from pipenv_poetry_migrate.migrate import PipenvPoetryMigration

app = typer.Typer()


def show_version(is_show: bool):
    if is_show:
        typer.echo(f"{__version__}")
        raise typer.Exit()


@app.command(context_settings=dict(help_option_names=["-h", "--help"]))
def main(
    pipfile: Path = typer.Option(
        ...,
        "--pipfile",
        "-f",
        help="path to Pipfile",
    ),
    pyproject_toml: Path = typer.Option(
        ...,
        "--pyproject-toml",
        "-t",
        help="path to pyproject.toml",
    ),
    use_group_notation: bool = typer.Option(
        True,
        "--use-group-notation/--no-use-group-notation",
        "--use-group/--no-use-group",
        help="migrate development dependencies with the new group notation",
    ),
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        "-n",
        help="dry-run",
    ),
    _: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="show version",
        callback=show_version,
        is_eager=True,
    ),
):
    """This is simple migration script, migrate pipenv to poetry"""
    try:
        PipenvPoetryMigration(
            pipfile,
            pyproject_toml,
            use_group_notation=use_group_notation,
            dry_run=dry_run,
        ).migrate()
    except PipfileNotFoundError:
        typer.secho(f"Pipfile '{pipfile}' not found", err=True, fg=typer.colors.RED)
        raise typer.Exit(code=1)
    except PyprojectTomlNotFoundError:
        typer.secho("Please run `poetry init` first", err=True, fg=typer.colors.RED)
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
