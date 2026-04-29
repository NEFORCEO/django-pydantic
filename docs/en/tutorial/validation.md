# Validation Errors

When request data fails Pydantic validation, django-pydantic-client returns a structured **HTTP 422 Unprocessable Entity** response automatically. This page explains the error format and how to customise it.

## How it works

`PydanticValidationMiddleware` is auto-installed by `django_pydantic`'s `AppConfig.ready()`. It hooks into Django's `process_exception` mechanism:

1. Your view calls `MySchema(request)`.
2. Pydantic raises `ValidationError` if data is invalid.
3. The middleware catches it before Django's 500 handler.
4. A `JsonResponse({"detail": [...]}, status=422)` is returned.

Your view function **never executes past the schema line** on invalid input.

## Error response format

```json
{
  "detail": [
    {
      "type":  "missing",
      "loc":   ["username"],
      "msg":   "Field required",
      "input": {}
    },
    {
      "type":  "string_too_short",
      "loc":   ["password"],
      "msg":   "String should have at least 8 characters",
      "input": "abc",
      "ctx":   {"min_length": 8}
    }
  ]
}
```

| Key | Description |
|-----|-------------|
| `type` | Pydantic error type identifier |
| `loc` | List of field names pointing to the failing field |
| `msg` | Human-readable error message |
| `input` | The value that was provided |
| `ctx` | Extra context (constraint values, etc.) |

## Multiple errors at once

Pydantic validates all fields before raising — you get **all errors in one response**, not just the first:

```bash
curl -X POST /signup/ \
     -H "Content-Type: application/json" \
     -d '{}'
```

```json
{
  "detail": [
    {"type": "missing", "loc": ["username"], "msg": "Field required"},
    {"type": "missing", "loc": ["email"],    "msg": "Field required"},
    {"type": "missing", "loc": ["age"],      "msg": "Field required"}
  ]
}
```

This is ideal for front-ends: one round-trip reveals all broken fields.

## Nested field locations

For nested models, `loc` is a path:

```python
class AddressSchema(BaseModel):
    city: str
    zip_code: str = Field(pattern=r"^\d{5}$")

class OrderSchema(RequestModel):
    address: AddressSchema
```

```json
{
  "detail": [
    {
      "type": "string_pattern_mismatch",
      "loc":  ["address", "zip_code"],
      "msg":  "String should match pattern '^\\d{5}$'"
    }
  ]
}
```

## Handling errors in the view (opt-in)

If you want to handle validation errors yourself instead of relying on the middleware, use a try/except:

```python
from pydantic import ValidationError
from django.http import JsonResponse

from .schema import SignupSchema


def signup(request):
    try:
        data = SignupSchema(request)
    except ValidationError as exc:
        # Custom error handling
        errors = {e["loc"][0]: e["msg"] for e in exc.errors(include_url=False)}
        return JsonResponse({"errors": errors}, status=400)

    # proceed...
    return JsonResponse({"ok": True})
```

!!! tip
    When you catch `ValidationError` yourself, the middleware is bypassed for that view.

## Custom error messages with Field

```python
from pydantic import Field
from django_pydantic import RequestModel


class SignupSchema(RequestModel):
    username: str = Field(
        min_length=3,
        max_length=32,
        description="3–32 characters, letters and numbers only",
    )
    age: int = Field(ge=18, description="Must be 18 or older")
```

Pydantic generates human-readable messages for all built-in constraints automatically.

## Custom validators

```python
from pydantic import field_validator
from django_pydantic import RequestModel


class SignupSchema(RequestModel):
    username: str
    password: str
    confirm_password: str

    @field_validator("username")
    @classmethod
    def username_alphanumeric(cls, v: str) -> str:
        if not v.isalnum():
            raise ValueError("Username must contain only letters and numbers")
        return v.lower()
```

Next: [URL Parameters →](url-params.md)
