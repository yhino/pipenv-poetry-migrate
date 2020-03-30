from argparse import ArgumentParser

from pipenv_poetry_migrate.migrate import migrate


def main():
    parser = ArgumentParser()
    parser.add_argument('-f', '--pipfile', type=str, required=True, help='path to Pipfile')
    parser.add_argument('-t', '--pyproject-toml', type=str, required=True, help='path to pyproject.toml')
    parser.add_argument('-n', '--dry-run', help='dry-run', action='store_true')
    args = parser.parse_args()

    migrate(
        args.pipfile,
        args.pyproject_toml,
        dry_run=args.dry_run,
    )


if __name__ == '__main__':
    main()
