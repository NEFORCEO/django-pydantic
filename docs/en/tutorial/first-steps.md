# First Steps

Let's build the simplest possible validated Django view, step by step.

## Install

```bash
pip install django-pydantic
```

## Add to INSTALLED_APPS

```python title="settings.py" hl_lines="4"
INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.auth",
    "django_pydantic",  # add this
    # your apps...
]
```

!!! success "Middleware auto-installs"
    You do **not** need to add anything to `MIDDLEWARE`. `django_pydantic` injects
    `PydanticValidationMiddleware` automatically when Django starts.

## Create a schema

Inside your Django app, create `schema.py`:

```python title="myapp/schema.py"
from django_pydantic import RequestModel


class HelloSchema(RequestModel):
    name: str
```

`RequestModel` is a `pydantic.BaseModel` subclass with one extra ability: it accepts a Django `HttpRequest` as its first argument.

## Write the view

```python title="myapp/views.py"
from django.http import JsonResponse

from .schema import HelloSchema


def hello(request):
    data = HelloSchema(request)  # (1)!
    return JsonResponse({"message": f"Hello, {data.name}!"})
```

1.  If `name` is missing or invalid, Pydantic raises `ValidationError`.
    The middleware catches it and returns **HTTP 422** automatically.
    Your view code never runs on invalid input.

## Register the URL

```python title="myapp/urls.py"
from django.urls import path

from .views import hello

urlpatterns = [
    path("hello/", hello),
]
```

## Try it

=== "GET request"

    ```bash
    curl "http://localhost:8000/hello/?name=Alice"
    ```

    ```json
    {"message": "Hello, Alice!"}
    ```

=== "POST JSON"

    ```bash
    curl -X POST http://localhost:8000/hello/ \
         -H "Content-Type: application/json" \
         -d '{"name": "Alice"}'
    ```

    ```json
    {"message": "Hello, Alice!"}
    ```

=== "POST form"

    ```bash
    curl -X POST http://localhost:8000/hello/ \
         -d "name=Alice"
    ```

    ```json
    {"message": "Hello, Alice!"}
    ```

## What happens on failure

```bash
curl "http://localhost:8000/hello/"
```

**HTTP 422 Unprocessable Entity:**

```json
{
  "detail": [
    {
      "type": "missing",
      "loc": ["name"],
      "msg": "Field required",
      "input": {}
    }
  ]
}
```

!!! tip
    The `loc` array tells the client exactly which field failed. Front-ends can use
    this to highlight the right input field without any extra work on your side.

## Summary

```python
from django_pydantic import RequestModel

class MySchema(RequestModel):   # (1)!
    field: type

def my_view(request):
    data = MySchema(request)    # (2)!
    ...                         # (3)!
```

1. Subclass `RequestModel` instead of `BaseModel`.
2. Pass `request` — data is extracted and validated automatically.
3. If you reach this line, `data` is guaranteed valid and fully typed.

Next: [Request Schema →](request-schema.md) — understand how this magic works.
