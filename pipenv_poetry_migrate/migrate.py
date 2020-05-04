from tomlkit import aot, dumps, inline_table, loads, table


def load_toml(filename):
    with open(filename, "r") as f:
        return loads(f.read())


class PipenvPoetryMigration(object):
    def __init__(self, pipfile, pyproject_toml, *, dry_run=False):
        self._pipenv = load_toml(pipfile)
        self._pyproject = load_toml(pyproject_toml)
        self._pyproject_toml = pyproject_toml
        self._dry_run = dry_run

    def migrate(self):
        self.migrate_source()
        self.migrate_dependencies()
        self.migrate_dev_dependencies()
        self.migrate_scripts()
        self.save()

    def save(self):
        if self._dry_run:
            print(dumps(self._pyproject))
        else:
            with open(self._pyproject_toml, "w") as f:
                f.write(dumps(self._pyproject))

    def migrate_source(self):
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

    def migrate_dependencies(self, *, dev=False):
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

    def migrate_dev_dependencies(self):
        self.migrate_dependencies(dev=True)

    def migrate_scripts(self):
        if "scripts" not in self._pipenv:
            return

        for name, cmd in self._pipenv["scripts"].items():
            if "scripts" not in self._pyproject["tool"]["poetry"]:
                self._pyproject["tool"]["poetry"]["scripts"] = table()
            self._pyproject["tool"]["poetry"]["scripts"].add(name, cmd)
