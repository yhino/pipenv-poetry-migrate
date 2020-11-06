<h1 align="center">pipenv-poetry-migrate</h1>
<p align="center">This is simple migration script, migrate pipenv to poetry.</p>

<p align="center">
    <a href="https://github.com/yhino/pipenv-poetry-migrate/actions?query=workflow%3Abuild"><img src="https://github.com/yhino/pipenv-poetry-migrate/workflows/build/badge.svg" alt="build"></a>
    <a href="https://app.fossa.com/projects/git%2Bgithub.com%2Fyhino%2Fpipenv-poetry-migrate?ref=badge_shield"><img src="https://app.fossa.com/api/projects/git%2Bgithub.com%2Fyhino%2Fpipenv-poetry-migrate.svg?type=shield" alt="FOSSA Status"></a>
</p>

## Setup

    $ pip install -U pipenv-poetry-migrate

## Migration

### Step 0: Install packages

    $ pip install poetry pipenv-poetry-migrate

### Step 1: Create `pyproject.toml` file

    $ poetry init

### Step 2: Migrate

To migrate `Pipfile` to `pyproject.toml`.

    $ pipenv-poetry-migrate -f Pipfile -t pyproject.toml

When want to run dry-run mode:

    $ pipenv-poetry-migrate -f Pipfile -t pyproject.toml -n

Dry-run mode is `pyproject.toml` file does not overwrite, results are displayed on standard output.

### Step 3: Generate lock file

    $ poetry lock

If there is already a `poetry.lock` file, remove it first.

### Step 4: Installing dependencies

To install the defined dependencies for your project.

    $ poetry install

## Example output

This is an example of a Pipfile to be migrated.

```toml
[[source]]
url = "https://pypi.python.org/simple"
verify_ssl = true
name = "pypi"

[packages]
requests = "*"

[dev-packages]
pytest = "^5.2"
```

Migrate the above file to the following pyproject.toml.

```toml
[tool.poetry]
name = "migration-sample"
version = "0.1.0"
description = ""
authors = ["Yoshiyuki HINO <yhinoz@gmail.com>"]

[tool.poetry.dependencies]
python = "^3.7"

[tool.poetry.dev-dependencies]

[build-system]
requires = ["poetry>=0.12"]
build-backend = "poetry.masonry.api"
```

By executing this script, pyproject.toml is rewritten as follows.

```toml
[tool.poetry]
name = "migration-sample"
version = "0.1.0"
description = ""
authors = ["Yoshiyuki HINO <yhinoz@gmail.com>"]

[tool.poetry.dependencies]
python = "^3.7"
requests = "*"

[tool.poetry.dev-dependencies]
pytest = "^5.2"

[build-system]
requires = ["poetry>=0.12"]
build-backend = "poetry.masonry.api"
```

## License
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Fyhino%2Fpipenv-poetry-migrate.svg?type=large)](https://app.fossa.com/projects/git%2Bgithub.com%2Fyhino%2Fpipenv-poetry-migrate?ref=badge_large)
