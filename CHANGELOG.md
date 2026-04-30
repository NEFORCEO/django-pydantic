# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Nothing yet.

## [0.1.2] - 2025-04-29

### Added
- `PydanticValidationMiddleware` auto-installed via `AppConfig.ready()`.
- `ModelResponse` generic `JsonResponse` wrapper for Pydantic models.
- `RequestModel` metaclass — instantiate directly from `HttpRequest`.
- Support for JSON body, form POST, and URL path parameters.
- Support for Django 4.2, 5.0, 5.1, 5.2.
- Support for Python 3.10, 3.11, 3.12, 3.13.
- MkDocs documentation with Material theme.
- PyPI publish workflow via GitHub Actions.

## [0.1.1] - 2025-04-29

### Fixed
- Package metadata corrections.

## [0.1.0] - 2025-04-29

### Added
- Initial release.
- `RequestModel` base class.
- `extract_data` helper for merging GET/POST/JSON/path params.

[Unreleased]: https://github.com/NEFORCEO/django-pydantic/compare/v0.1.2...HEAD
[0.1.2]: https://github.com/NEFORCEO/django-pydantic/compare/v0.1.1...v0.1.2
[0.1.1]: https://github.com/NEFORCEO/django-pydantic/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/NEFORCEO/django-pydantic/releases/tag/v0.1.0
