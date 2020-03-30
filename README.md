# pipenv-poetry-migrate

This is simple migration script, migrate pipenv to poetry.

## Usage

    $ pipenv-poetry-migrate -f Pipfile -t pyproject.toml

## Example

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