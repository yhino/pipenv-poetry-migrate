<h1 align="center">pipenv-poetry-migrate</h1>
<p align="center">This is simple migration script, migrate pipenv to poetry.</p>

<p align="center">
    <a href="https://pypi.org/project/pipenv-poetry-migrate/"><img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/pipenv-poetry-migrate"></a>
    <a href="https://pypi.org/project/pipenv-poetry-migrate/"><img src="https://img.shields.io/pypi/dm/pipenv-poetry-migrate" alt="PyPI - Downloads"></a>
    <a href="https://github.com/yhino/pipenv-poetry-migrate/actions?query=workflow%3Abuild"><img src="https://github.com/yhino/pipenv-poetry-migrate/workflows/build/badge.svg" alt="build"></a>
    <a href="https://codecov.io/gh/yhino/pipenv-poetry-migrate"><img src="https://codecov.io/gh/yhino/pipenv-poetry-migrate/branch/main/graph/badge.svg?token=LHZGQ8MMWT" alt="Codecov"></a>
    <a href="https://app.fossa.com/projects/git%2Bgithub.com%2Fyhino%2Fpipenv-poetry-migrate?ref=badge_shield"><img src="https://app.fossa.com/api/projects/git%2Bgithub.com%2Fyhino%2Fpipenv-poetry-migrate.svg?type=shield" alt="FOSSA Status"></a>
</p>

## :rocket: Get Started

### Installation

    $ pip install -U poetry pipenv-poetry-migrate

### Migration

#### Step 1: Create `pyproject.toml` file

    $ poetry init

#### Step 2: Migrate

To migrate `Pipfile` to `pyproject.toml`.

    $ pipenv-poetry-migrate -f Pipfile -t pyproject.toml

When want to run dry-run mode:

    $ pipenv-poetry-migrate -f Pipfile -t pyproject.toml -n

Dry-run mode is `pyproject.toml` file does not overwrite, results are displayed on standard output.

> **Note**  
> If the dependency already exists in the poetry dependency and you want to re-migrate it, please use the `--re-migrate` option.
> However, if the dependency is removed from pipenv, the poetry dependency is not removed.
>
>     $ pipenv-poetry-migrate -f Pipfile -t pyproject.toml --re-migrate

> **Note**  
> The default behavior is to migrate with the [group notation](https://python-poetry.org/docs/master/managing-dependencies/#dependency-groups), which has been available since Poetry 1.2.0.
> If you want to migrate with `dev-dependencies` notation, please use the `--on-use-group-notation` option.
> 
>     $ pipenv-poetry-migrate -f Pipfile -t pyproject.toml --no-use-group-notation

#### Step 3: Generate lock file

    $ poetry lock

If there is already a `poetry.lock` file, remove it first.

#### Step 4: Installing dependencies

To install the defined dependencies for your project.

    $ poetry install

### Example output

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

[tool.poetry.group.dev.dependencies]

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
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

[tool.poetry.group.dev.dependencies]
pytest = "^5.2"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

## :handshake: Contributing

1. Fork and clone the repository, and create the development branch.
2. Run `poetry install` to setup your develop environment.
3. Do your code.
4. Run `bash scripts/test.sh` to check that your test passed.
5. Run `bash scripts/format.sh` and `bash scripts/lint.sh` to check that you haven't warnings.
6. Open a PR on GitHub.

### Test cases

Test cases are in `tests/toml`, update `Pipfile` with additional entries and `expect_pyproject.toml` with expected output.


## :pencil: License

[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Fyhino%2Fpipenv-poetry-migrate.svg?type=large)](https://app.fossa.com/projects/git%2Bgithub.com%2Fyhino%2Fpipenv-poetry-migrate?ref=badge_large)
