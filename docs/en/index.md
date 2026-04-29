# django-pydantic-client

**django-pydantic-client** lets you replace manual request parsing with Pydantic models. Pass a Django `HttpRequest` directly to your schema and get a fully validated, typed Python object back — or an automatic HTTP 422 response if validation fails.

## Features

- **One-line validation** — `data = MySchema(request)`
- **Automatic error responses** — middleware converts `ValidationError` to `422 JSON`
- **Smart data merging** — GET params + POST/JSON body + URL kwargs, all in one object
- **Zero config** — middleware auto-installs via `INSTALLED_APPS`
- **Full Pydantic v2** — validators, `Field()`, custom types, `model_config`

## Requirements

| Dependency | Version |
|------------|---------|
| Python     | ≥ 3.10  |
| Django     | ≥ 4.2   |
| Pydantic   | ≥ 2.0   |

## Installation

```bash
pip install django-pydantic-client
```

```python title="settings.py"
INSTALLED_APPS = [
    ...
    "django_pydantic",
]
```

That's it. Ready to use.

## Where to go next

- [**Tutorial → First Steps**](tutorial/first-steps.md) — build your first validated view
- [**Tutorial → Request Schema**](tutorial/request-schema.md) — how `RequestModel` works under the hood
- [**API Reference**](reference/request-model.md) — full `RequestModel` reference
