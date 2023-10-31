from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any

import typer
from tomlkit import aot, dumps, inline_table, nl, table

if TYPE_CHECKING:
    from tomlkit.items import InlineTable, Item

from pipenv_poetry_migrate.loader import load_pipfile, load_pyproject_toml
from pipenv_poetry_migrate.translator import translate_properties


@dataclass
class MigrationOption:
    use_group_notation: bool = True
    re_migrate: bool = False
    dry_run: bool = False


class PipenvPoetryMigration:
    def __init__(
        self,
        pipfile: Path,
        pyproject_toml: Path,
        *,
        option: MigrationOption,
    ) -> None:
        self._pipenv = load_pipfile(pipfile)
        self._pyproject = load_pyproject_toml(pyproject_toml)
        self._pyproject_tool = self._pyproject.get("tool", table(is_super_table=True))
        self._poetry = self._pyproject_tool.get("poetry", table())
        self._pyproject_toml = pyproject_toml
        self._option = option

    def pyproject_toml(self) -> Path:
        return self._pyproject_toml

    def migrate(self) -> None:
        self._migrate_dependencies()
        self._migrate_dev_dependencies()
        self._migrate_scripts()
        self._migrate_source()
        self._save()

    def _save(self) -> None:
        if self._option.dry_run:
            typer.echo(dumps(self._pyproject))
        else:
            with Path(self._pyproject_toml).open("w") as f:
                f.write(dumps(self._pyproject))

    def _migrate_dependencies(
        self,
        *,
        pipenv_key: str = "packages",
        poetry_key: str = "dependencies",
    ) -> None:
        if poetry_key not in self._poetry:
            self._poetry.add(poetry_key, table())

        for raw_name, properties in self._pipenv.get(pipenv_key, {}).items():
            name, extras = self._split_extras(raw_name)
            formatted_properties = self._reformat_dependency_properties(
                extras,
                properties,
            )
            if name in self._poetry[poetry_key]:
                if not self._option.re_migrate:
                    continue
                self._poetry[poetry_key][name] = formatted_properties
            else:
                self._poetry[poetry_key].add(name, formatted_properties)

    def _migrate_dependency_groups(self, pipenv_key: str, group_name: str) -> None:
        if "group" not in self._poetry:
            self._poetry["group"] = table(is_super_table=True)
        if group_name not in self._poetry["group"]:
            self._poetry["group"][group_name] = table(is_super_table=True).add(
                "dependencies",
                table(),
            )

        group = self._poetry["group"][group_name]
        for raw_name, properties in self._pipenv.get(pipenv_key, {}).items():
            name, extras = self._split_extras(raw_name)
            formatted_properties = self._reformat_dependency_properties(
                extras,
                properties,
            )
            if name in group["dependencies"]:
                if not self._option.re_migrate:
                    continue
                group["dependencies"][name] = formatted_properties
            else:
                group["dependencies"].add(name, formatted_properties)
        group.add(nl())

    def _migrate_dev_dependencies(self) -> None:
        if self._option.use_group_notation:
            self._migrate_dependency_groups(pipenv_key="dev-packages", group_name="dev")

            # if there is no dependency, remove the traditional notation
            if (
                "dev-dependencies" in self._poetry
                and len(self._poetry["dev-dependencies"]) < 1
            ):
                self._poetry.remove("dev-dependencies")
        else:
            self._migrate_dependencies(
                pipenv_key="dev-packages",
                poetry_key="dev-dependencies",
            )

    def _migrate_scripts(self) -> None:
        if "scripts" not in self._pipenv:
            return
        typer.secho(
            ">>>WARNING<<< poetry does not have the function of task runner."
            " migration of the scripts section will be skipped.",
            err=True,
            fg=typer.colors.YELLOW,
        )

    def _migrate_source(self) -> None:
        for s in self._pipenv.get("source", aot()):
            if s["name"] == "pypi":
                continue

            source = table()
            source.add("name", s["name"])
            source.add("url", s["url"])
            source.add(nl())

            if "source" not in self._poetry:
                self._poetry["source"] = aot()
            self._poetry["source"].append(source)

    @staticmethod
    def _split_extras(name: str) -> tuple[str, str | None]:
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
        extras: str | None,
        properties: str | dict[str, Any],
    ) -> Item | InlineTable:
        formatted = inline_table()
        if extras is not None:
            formatted.update({"extras": extras.split(",")})
        if isinstance(properties, dict):
            formatted.update(translate_properties(properties))
        else:
            formatted.append("version", properties)
        return (
            formatted["version"]
            if len(formatted) == 1 and "version" in formatted
            else formatted
        )
