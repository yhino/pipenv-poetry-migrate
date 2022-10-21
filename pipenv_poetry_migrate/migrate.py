import re
from pathlib import Path
from typing import Any, Dict, Optional, Tuple, Union

import typer
from tomlkit import aot, dumps, inline_table, nl, table
from tomlkit.container import Container
from tomlkit.items import InlineTable, Table, Trivia

from pipenv_poetry_migrate.loader import load_pipfile, load_pyproject_toml
from pipenv_poetry_migrate.translator import translate_properties


class PipenvPoetryMigration:
    def __init__(
        self,
        pipfile: Path,
        pyproject_toml: Path,
        *,
        use_group_notation: bool = False,
        dry_run: bool = False
    ):
        self._pipenv = load_pipfile(pipfile)
        self._pyproject = load_pyproject_toml(pyproject_toml)
        self._pyproject_toml = pyproject_toml
        self._use_group_notation = use_group_notation
        self._dry_run = dry_run

    def pyproject_toml(self) -> Path:
        return self._pyproject_toml

    def migrate(self):
        self._migrate_source()
        self._migrate_dependencies()
        self._migrate_dev_dependencies()
        self._migrate_scripts()
        self._save()

    def _save(self):
        if self._dry_run:
            print(dumps(self._pyproject))
        else:
            with open(self._pyproject_toml, "w") as f:
                f.write(dumps(self._pyproject))

    def _migrate_source(self):
        if "source" not in self._pipenv:
            return

        for s in self._pipenv["source"]:
            if s["name"] == "pypi":
                continue

            source = table()
            source.add("name", s["name"])
            source.add("url", s["url"])
            source.add(nl())

            if "source" not in self._pyproject["tool"]["poetry"]:
                self._pyproject["tool"]["poetry"]["source"] = aot()
            self._pyproject["tool"]["poetry"]["source"].append(source)

    def _migrate_dependencies(
        self, *, pipenv_key: str = "packages", poetry_key: str = "dependencies"
    ):
        if poetry_key not in self._pyproject["tool"]["poetry"]:
            self._pyproject["tool"]["poetry"].add(poetry_key, table())

        for name, properties in self._pipenv.get(pipenv_key, {}).items():
            name, extras = self._split_extras(name)
            if name in self._pyproject["tool"]["poetry"][poetry_key]:
                continue
            properties = self._reformat_dependency_properties(extras, properties)
            self._pyproject["tool"]["poetry"][poetry_key].add(name, properties)

    def _migrate_dependency_groups(self, pipenv_key: str, group_name: str):
        if "group" not in self._pyproject["tool"]["poetry"]:
            self._pyproject["tool"]["poetry"]["group"] = Table(
                Container(), Trivia(), False, is_super_table=True
            )
        if group_name not in self._pyproject["tool"]["poetry"]["group"]:
            self._pyproject["tool"]["poetry"]["group"][group_name] = Table(
                Container(), Trivia(), False, is_super_table=True
            ).add("dependencies", table())

        group = self._pyproject["tool"]["poetry"]["group"][group_name]
        for name, properties in self._pipenv.get(pipenv_key, {}).items():
            name, extras = self._split_extras(name)
            if name in group["dependencies"]:
                continue
            properties = self._reformat_dependency_properties(extras, properties)
            group["dependencies"].add(name, properties)
        self._pyproject["tool"]["poetry"]["group"][group_name] = group

    def _migrate_dev_dependencies(self):
        if self._use_group_notation:
            self._migrate_dependency_groups(pipenv_key="dev-packages", group_name="dev")

            # if there is no dependency, remove the traditional notation
            if (
                "dev-dependencies" in self._pyproject["tool"]["poetry"]
                and len(self._pyproject["tool"]["poetry"]["dev-dependencies"]) < 1
            ):
                self._pyproject["tool"]["poetry"].remove("dev-dependencies")
        else:
            self._migrate_dependencies(
                pipenv_key="dev-packages", poetry_key="dev-dependencies"
            )

    def _migrate_scripts(self):
        if "scripts" not in self._pipenv:
            return
        typer.secho(
            ">>>WARNING<<< poetry does not have the function of task runner."
            " migration of the scripts section will be skipped.",
            err=True,
            fg=typer.colors.YELLOW,
        )

    @staticmethod
    def _split_extras(name: str) -> Tuple[str, Optional[str]]:
        m = re.match(r"^(.+)\[([^\]]+)\]$", name)
        extras = None
        if m:
            name_no_extras = m.group(1)
            extras = m.group(2)
        else:
            name_no_extras = name

        return name_no_extras, extras

    @staticmethod
    def _reformat_dependency_properties(
        extras: Optional[str], properties: Union[str, Dict[str, Any]]
    ) -> Union[str, InlineTable]:
        formatted = inline_table()
        if extras is not None:
            formatted.update({"extras": extras.split(",")})
        if isinstance(properties, dict):
            formatted.update(translate_properties(properties))
        else:
            formatted.append("version", properties)
        return (
            formatted["version"]
            if len(formatted) == 1 and "version" in formatted.keys()
            else formatted
        )
