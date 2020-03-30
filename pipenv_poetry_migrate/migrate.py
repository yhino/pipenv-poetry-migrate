from tomlkit import loads, dumps, table, inline_table, aot


def load(filename):
    with open(filename, 'r') as f:
        return loads(f.read())


def save(filename, toml, *, dry_run=False):
    if dry_run:
        print(dumps(toml))
        return

    with open(filename, 'w') as f:
        f.write(dumps(toml))


def migrate(pipfile, pyproject_toml, *, dry_run=False):
    pipenv = load(pipfile)
    pyproject = load(pyproject_toml)

    migrate_source_repo(pipenv, pyproject)
    migrate_dependencies(pipenv, pyproject)
    migrate_dependencies(pipenv, pyproject, dev=True)
    migrate_scripts(pipenv, pyproject)

    save(pyproject_toml, pyproject, dry_run=dry_run)


def migrate_source_repo(pipenv, pyproject):
    if 'source' not in pipenv:
        return

    for s in pipenv['source']:
        if s['name'] == 'pypi':
            continue

        source = table()
        source.add('name', s['name'])
        source.add('url', s['url'])

        if 'source' not in pyproject['tool']['poetry']:
            pyproject['tool']['poetry']['source'] = aot()
        pyproject['tool']['poetry']['source'].add(source)


def migrate_dependencies(pipenv, pyproject, *, dev=False):
    prefix = 'dev-' if dev else ''
    pipenv_key = prefix + 'packages'
    poetry_key = prefix + 'dependencies'

    for name, ver in pipenv[pipenv_key].items():
        if name in pyproject['tool']['poetry'][poetry_key]:
            continue
        if isinstance(ver, dict):
            tmp = inline_table()
            tmp.update(ver)
            ver = tmp
        pyproject['tool']['poetry'][poetry_key].add(name, ver)


def migrate_scripts(pipenv, pyproject):
    if 'scripts' not in pipenv:
        return

    for name, cmd in pipenv['scripts'].items():
        if 'scripts' not in pyproject['tool']['poetry']:
            pyproject['tool']['poetry']['scripts'] = table()
        pyproject['tool']['poetry']['scripts'].add(name, cmd)