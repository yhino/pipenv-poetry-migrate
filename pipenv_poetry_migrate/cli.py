import sys
from argparse import ArgumentParser

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
    parser.add_argument("-n", "--dry-run", help="dry-run", action="store_true")
    args = parser.parse_args()

    try:
        PipenvPoetryMigration(
            args.pipfile,
            args.pyproject_toml,
            dry_run=args.dry_run,
        ).migrate()
    except PipfileNotFoundError:
        print(f"Pipfile '{args.pipfile}' not found")
        sys.exit(1)
    except PyprojectTomlNotFoundError:
        print("Please run `poetry init` first")
        sys.exit(1)


if __name__ == "__main__":
    main()
