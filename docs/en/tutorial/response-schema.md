# Response Schema

Just as you validate **incoming** data with `RequestModel`, you can validate and serialize **outgoing** data with `ModelResponse`.

## Define a response schema

```python title="myapp/schema.py"
from uuid import UUID

from django_pydantic import RequestModel


class HelloRequest(RequestModel):
    name: str


class HelloResponse(RequestModel):
    id: UUID
    message: str
```

`RequestModel` is still just a Pydantic `BaseModel`, so you can use it for responses too — field types, validators, and serialization all work the same way.

## Return ModelResponse from the view

```python title="myapp/views.py"
from uuid import uuid4

from django.http import HttpRequest

from django_pydantic import ModelResponse

from .schema import HelloRequest, HelloResponse


def hello(request: HttpRequest) -> ModelResponse[HelloResponse]:
    data = HelloRequest(request)
    return ModelResponse(
        HelloResponse(id=uuid4(), message=f"Hello, {data.name}!")
    )
```

`ModelResponse` wraps a Pydantic model instance in a JSON response. The type parameter `ModelResponse[HelloResponse]` gives the type checker everything it needs.

## What you get

- **Pydantic serialization** — `UUID`, `datetime`, `Decimal`, custom types all serialize correctly via `model_dump_json()`.
- **Type-safe return annotation** — `ModelResponse[HelloResponse]` makes the return type explicit. IDEs autocomplete the fields.
- **Validation on construction** — `HelloResponse(...)` validates before it ever reaches the response, so invalid outgoing data raises early.

## Response format

```bash
curl "http://localhost:8000/hello/?name=Alice"
```

```json
{
  "id": "a1b2c3d4-...",
  "message": "Hello, Alice!"
}
```

## Optional: status code

```python
return ModelResponse(HelloResponse(...), status=201)
```

## Compared to plain JsonResponse

| | `JsonResponse(dict)` | `ModelResponse(schema)` |
|---|---|---|
| Type-safe | No | Yes |
| UUID / datetime / Decimal | Via `DjangoJSONEncoder` | Via Pydantic |
| Validated output | No | Yes |
| IDE autocomplete | No | Yes |

Next: [URL Parameters →](url-params.md)
