# Contributing

## Setup

```bash
git clone https://github.com/NEFORCEO/django-pydantic.git
cd django-pydantic
uv sync
```

## Running Tests

```bash
cd test_app
uv run python manage.py test
```

## Code Style

This project uses [Ruff](https://docs.astral.sh/ruff/) for linting and formatting.

```bash
uv run ruff check .
uv run ruff format .
```

Type checking with mypy:

```bash
uv run mypy django_pydantic/
```

## Pull Request Process

1. Fork the repository.
2. Create a branch: `git checkout -b feat/your-feature`.
3. Make your changes with tests.
4. Run the full test suite and linters.
5. Update `CHANGELOG.md` under `[Unreleased]`.
6. Open a pull request against `master`.

## Commit Convention

Use [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add file upload support
fix: handle empty JSON body
docs: update RequestModel example
chore: bump pydantic to 2.7
```

## Versioning

This project uses [Semantic Versioning](https://semver.org/). Version is set in `pyproject.toml`.
A new Git tag and PyPI release are created automatically on merge to `master` when the version changes.
