# RequestModel

```python
from django_pydantic import RequestModel
```

A `pydantic.BaseModel` subclass that can be instantiated directly from a Django `HttpRequest`.

---

## Class: RequestModel

**Bases:** `pydantic.BaseModel`

### Instantiation

#### `MySchema(request, **kwargs)`

```python
data = MySchema(request)
data = MySchema(request, pk=pk)   # merge URL kwargs
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `request` | `django.http.HttpRequest` | The current request. Data is extracted automatically. |
| `**kwargs` | `Any` | Extra key-value pairs merged with highest priority (URL path params). |

**Returns:** A validated instance of `MySchema`.

**Raises:** `pydantic.ValidationError` if validation fails. The auto-installed middleware converts this to HTTP 422.

---

#### `MySchema(field=value, ...)`

Standard Pydantic instantiation still works:

```python
data = MySchema(username="alice", email="alice@example.com")
```

---

### Classmethods

#### `MySchema._extract(request, **kwargs) → dict`

Override this classmethod to customise how data is extracted from the request. The default calls `django_pydantic.request.extract_data`.

```python
class MySchema(RequestModel):
    @classmethod
    def _extract(cls, request, **extra):
        from django_pydantic.request import extract_data
        data = extract_data(request, **extra)
        data["user_id"] = request.user.pk   # inject extra fields
        return data
```

---

### Inherited from BaseModel

All standard Pydantic methods are available:

| Method | Description |
|--------|-------------|
| `model_dump(**kw)` | Serialize to `dict` |
| `model_dump_json(**kw)` | Serialize to JSON string |
| `model_copy(**kw)` | Return a copy with optional field overrides |
| `model_fields_set` | Set of field names explicitly provided |
| `model_validate(data)` | Class method — validate from dict |
| `model_json_schema()` | Return JSON Schema dict |

---

## Function: extract_data

```python
from django_pydantic.request import extract_data
```

```python
def extract_data(request: HttpRequest, **extra: Any) -> dict
```

Builds a flat `dict` from a Django `HttpRequest` by merging:

1. `request.GET` query parameters
2. JSON body (if `Content-Type: application/json`)  
   — OR — `request.POST` form data (for non-GET/HEAD/OPTIONS/DELETE)
3. `**extra` keyword arguments (highest priority)

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `request` | `HttpRequest` | Django request object |
| `**extra` | `Any` | Extra fields merged last (e.g. URL path params) |

**Returns:** `dict` ready for `pydantic.BaseModel.model_validate`.

---

## Class: PydanticValidationMiddleware

```python
from django_pydantic.middleware import PydanticValidationMiddleware
```

Django middleware that catches `pydantic.ValidationError` raised during request handling and returns a structured 422 JSON response.

**Auto-installed** when `django_pydantic` is in `INSTALLED_APPS`. You do not need to add it manually to `settings.MIDDLEWARE`.

### Response format

```json
{
  "detail": [
    {
      "type":  "string",
      "loc":   ["field_name"],
      "msg":   "string",
      "input": "any"
    }
  ]
}
```

### Manual installation

If you need to control middleware order, add it explicitly and it won't be auto-inserted again:

```python title="settings.py"
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django_pydantic.middleware.PydanticValidationMiddleware",  # (1)!
    ...
]
```

1. django-pydantic-client checks if it's already present and skips auto-insertion.
