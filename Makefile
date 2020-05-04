clean:
	@rm -rf build dist .eggs *.egg-info
	@rm -rf .coverage coverage.xml htmlcov report.xml .tox
	@find . -type d -name '.mypy_cache' -exec rm -rf {} +
	@find . -type d -name '__pycache__' -exec rm -rf {} +
	@find . -type d -name '*pytest_cache*' -exec rm -rf {} +
	@find . -type d -name '*.py[co]' -exec rm -rf {} +

format: clean
	@poetry run black .
	@poetry run isort -y

test:
	@poetry run pytest --verbose \
		--cov=pipenv_poetry_migrate \
		--cov-report=term \
		--cov-report=xml \
		--cov-report=html \
		tests

tox:
	@tox
