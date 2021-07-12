import re
import sys
from typing import Any, Dict, Optional, Tuple, Union

import rich
from tomlkit import aot, dumps, inline_table, table
from tomlkit.items import InlineTable

from pipenv_poetry_migrate.loader import load_pipfile, load_pyproject_toml
from pipenv_poetry_migrate.translator import translate_properties


class PipenvPoetryMigration(object):
    def __init__(self, pipfile: str, pyproject_toml: str, *, dry_run: bool = False):
        self._pipenv = load_pipfile(pipfile)
        self._pyproject = load_pyproject_toml(pyproject_toml)
        self._pyproject_toml = pyproject_toml
        self._dry_run = dry_run

    def pyproject_toml(self) -> str:
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

            if "source" not in self._pyproject["tool"]["poetry"]:
                self._pyproject["tool"]["poetry"]["source"] = aot()
            self._pyproject["tool"]["poetry"]["source"].append(source)

    def _migrate_dependencies(self, *, dev: bool = False):
        prefix = "dev-" if dev else ""
        pipenv_key = prefix + "packages"
        poetry_key = prefix + "dependencies"

        for name, properties in self._pipenv.get(pipenv_key, {}).items():
            name, extras = self._split_extras(name)
            if name in self._pyproject["tool"]["poetry"][poetry_key]:
                continue
            properties = self._reformat_dependency_properties(extras, properties)
            self._pyproject["tool"]["poetry"][poetry_key].add(name, properties)

    def _migrate_dev_dependencies(self):
        self._migrate_dependencies(dev=True)

    def _migrate_scripts(self):
        if "scripts" not in self._pipenv:
            return
        rich.print(
            "[yellow]!!WARNING!! poetry does not have the function of task runner."
            " migration of the scripts section will be skipped.",
            file=sys.stderr,
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
