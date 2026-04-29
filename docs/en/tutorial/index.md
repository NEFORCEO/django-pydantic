# Tutorial — User Guide

This tutorial walks you through every feature of **django-pydantic-client**, from installation to advanced usage.

Each section builds on the previous one. You can read it from start to finish or jump to the topic you need.

## Sections

| Section | What you learn |
|---------|----------------|
| [First Steps](first-steps.md) | Install, setup, write your first validated view |
| [Request Schema](request-schema.md) | How `RequestModel` works internally |
| [Request Data Sources](request-data.md) | Where data comes from: JSON, form, GET, URL params |
| [Validation Errors](validation.md) | 422 responses, error format, custom error handling |
| [URL Parameters](url-params.md) | Pass path kwargs into the schema |
| [Pydantic Features](pydantic-features.md) | `Field()`, validators, `model_config`, computed fields |

## Assumed knowledge

- Basic Django: views, URLs, `HttpRequest`
- Basic Pydantic: `BaseModel`, type annotations

No knowledge of Django REST Framework required.
