from tomlkit import aot, dumps, inline_table, table

from pipenv_poetry_migrate.loader import load_pipfile, load_pyproject_toml


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

        for name, ver in self._pipenv[pipenv_key].items():
            if name in self._pyproject["tool"]["poetry"][poetry_key]:
                continue
            if isinstance(ver, dict):
                tmp = inline_table()
                tmp.update(ver)
                ver = tmp
            self._pyproject["tool"]["poetry"][poetry_key].add(name, ver)

    def _migrate_dev_dependencies(self):
        self._migrate_dependencies(dev=True)

    def _migrate_scripts(self):
        if "scripts" not in self._pipenv:
            return

        for name, cmd in self._pipenv["scripts"].items():
            if "scripts" not in self._pyproject["tool"]["poetry"]:
                self._pyproject["tool"]["poetry"]["scripts"] = table()
            self._pyproject["tool"]["poetry"]["scripts"].add(name, cmd)
