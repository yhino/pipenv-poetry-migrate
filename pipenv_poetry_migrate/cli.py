import sys
from argparse import ArgumentParser

import rich

from pipenv_poetry_migrate import __version__
from pipenv_poetry_migrate.loader import (
    PipfileNotFoundError,
    PyprojectTomlNotFoundError,
)
from pipenv_poetry_migrate.migrate import PipenvPoetryMigration


def main():
    parser = ArgumentParser()
    parser.add_argument(
        "-f", "--pipfile", type=str, required=True, help="path to Pipfile"
    )
    parser.add_argument(
        "-t", "--pyproject-toml", type=str, required=True, help="path to pyproject.toml"
    )
    parser.add_argument(
        "--use-group-notation",
        "--use-group",
        help="migrate development dependencies with the new group notation",
        action="store_true",
    )
    parser.add_argument("-n", "--dry-run", help="dry-run", action="store_true")
    parser.add_argument(
        "-v", "--version", help="show version", action="version", version=__version__
    )
    args = parser.parse_args()

    try:
        PipenvPoetryMigration(
            args.pipfile,
            args.pyproject_toml,
            use_group_notation=args.use_group_notation,
            dry_run=args.dry_run,
        ).migrate()
    except PipfileNotFoundError:
        rich.print(f"[red]Pipfile '{args.pipfile}' not found", file=sys.stderr)
        sys.exit(1)
    except PyprojectTomlNotFoundError:
        rich.print("[red]Please run `poetry init` first", file=sys.stderr)
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
