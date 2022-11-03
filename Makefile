NEW_VERSION := $(shell poetry run semantic-release print-version 2>/dev/null)

release:
ifneq ($(NEW_VERSION),)
	@git ci --allow-empty --message=":bookmark: $(NEW_VERSION)"
endif

clean:
	@rm -rf build dist .eggs *.egg-info
	@rm -rf .coverage coverage.xml htmlcov report.xml .tox
	@find . -type d -name '.mypy_cache' -exec rm -rf {} +
	@find . -type d -name '__pycache__' -exec rm -rf {} +
	@find . -type d -name '*pytest_cache*' -exec rm -rf {} +
	@find . -type f -name '*.py[co]' -exec rm -rf {} +

format: clean
	@poetry run black --version
	@poetry run black .
	@echo "isort, version `poetry run isort --vn`"
	@poetry run isort .

lint: clean
	@poetry run black --version
	@poetry run black --check .
	@poetry run flake8 --version
	@poetry run flake8
	@poetry run mypy --version
	@poetry run mypy .

test: clean
	@poetry run pytest -vv \
		--cov=pipenv_poetry_migrate \
		--cov-report=term \
		--cov-report=xml \
		--cov-report=html \
		tests
