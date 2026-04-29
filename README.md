<p align="center">
  <a href="https://django-pydantic.readthedocs.io">
    <img src="https://raw.githubusercontent.com/NEFORCEO/django-pydantic/master/docs/stylesheets/logo.svg" alt="django-pydantic" width="200">
  </a>
</p>

<p align="center">
  <em>Skip the serializer. Validate Django requests with Pydantic models — one line, zero boilerplate.</em>
</p>

<p align="center">
  <a href="https://github.com/NEFORCEO/django-pydantic/actions/workflows/publish.yml">
    <img src="https://github.com/NEFORCEO/django-pydantic/actions/workflows/publish.yml/badge.svg" alt="CI / Publish">
  </a>
  <a href="https://pypi.org/project/django-pydantic/">
    <img src="https://img.shields.io/pypi/v/django-pydantic?color=%2344B78B&label=pypi" alt="PyPI version">
  </a>
  <a href="https://pypi.org/project/django-pydantic/">
    <img src="https://img.shields.io/pypi/pyversions/django-pydantic?color=%2344B78B" alt="Python versions">
  </a>
  <a href="https://pypi.org/project/django-pydantic/">
    <img src="https://img.shields.io/pypi/dm/django-pydantic?color=%2344B78B" alt="Downloads">
  </a>
  <a href="https://github.com/NEFORCEO/django-pydantic/blob/master/LICENSE">
    <img src="https://img.shields.io/github/license/NEFORCEO/django-pydantic?color=%2344B78B" alt="License">
  </a>
</p>

---

**Documentation**: <a href="https://django-pydantic.readthedocs.io" target="_blank">https://django-pydantic.readthedocs.io</a>

**Source Code**: <a href="https://github.com/NEFORCEO/django-pydantic" target="_blank">https://github.com/NEFORCEO/django-pydantic</a>

---

**django-pydantic** lets you replace manual request parsing in Django views with Pydantic models. Pass a `HttpRequest` directly to your schema — get a fully validated, typed Python object back, or an automatic HTTP 422 response if validation fails.

Key features:

- **One-line validation** — `data = MySchema(request)`
- **Automatic 422 errors** — middleware converts `ValidationError` to structured JSON, no try/except needed
- **Smart data merging** — GET params + POST form / JSON body + URL kwargs, all in one object
- **Zero configuration** — middleware auto-installs via `INSTALLED_APPS`, nothing else to do
- **Full Pydantic v2** — validators, `Field()`, `model_config`, computed fields, custom types

## Requirements

- Python 3.10+
- Django 4.2+
- Pydantic 2.0+

## Installation

```bash
pip install django-pydantic
```

Add to `INSTALLED_APPS` — that's the only configuration step:

```python
# settings.py
INSTALLED_APPS = [
    ...
    "django_pydantic",
]
```

`PydanticValidationMiddleware` is injected automatically. You do not need to touch `MIDDLEWARE`.

## Quick start

**Define a schema:**

```python
# myapp/schema.py
from pydantic import EmailStr, Field
from django_pydantic import RequestModel


class SignupSchema(RequestModel):
    username: str = Field(min_length=3, max_length=32)
    email: EmailStr
    age: int = Field(ge=18)
```

**Use it in a view:**

```python
# myapp/views.py
from django.http import JsonResponse
from .schema import SignupSchema


def signup(request):
    data = SignupSchema(request)          # validates GET / POST / JSON body
    # data.username, data.email, data.age — typed and validated
    return JsonResponse({"username": data.username})
```

**Wire up the URL:**

```python
# urls.py
from django.urls import path
from myapp.views import signup

urlpatterns = [
    path("signup/", signup),
]
```

On invalid input the response is automatic — no extra code required:

```json
{
  "detail": [
    {"type": "missing",     "loc": ["username"], "msg": "Field required"},
    {"type": "value_error", "loc": ["email"],    "msg": "value is not a valid email address"}
  ]
}
```

## How data sources are merged

| Source | When used |
|--------|-----------|
| `request.GET` | Always (any HTTP method) |
| `request.POST` | Non-GET/HEAD/DELETE, no JSON content-type |
| JSON body | `Content-Type: application/json` |
| URL kwargs | Passed explicitly: `MySchema(request, pk=pk)` |

Later sources override earlier ones. URL kwargs always win.

## URL path parameters

```python
# urls.py
path("users/<int:pk>/", user_detail)

# views.py
def user_detail(request, pk):
    data = UserSchema(request, pk=pk)    # pk merged with highest priority
    user = User.objects.get(pk=data.pk)
    ...
```

## Full Pydantic v2 support

```python
from pydantic import Field, field_validator, computed_field
from django_pydantic import RequestModel


class OrderSchema(RequestModel):
    product_id: int = Field(gt=0)
    quantity: int   = Field(ge=1, le=100)
    coupon: str     = ""

    @field_validator("coupon")
    @classmethod
    def normalise_coupon(cls, v: str) -> str:
        return v.strip().upper()

    @computed_field
    @property
    def total_label(self) -> str:
        return f"{self.quantity}x product #{self.product_id}"
```

## Class-based views

```python
from django.views import View
from django.http import JsonResponse
from .schema import ArticleCreateSchema


class ArticleView(View):

    def post(self, request):
        data = ArticleCreateSchema(request)
        article = Article.objects.create(
            title=data.title,
            body=data.body,
            author=request.user,
        )
        return JsonResponse({"id": article.pk}, status=201)
```

## Error handling (opt-in)

The middleware handles errors automatically. To customise for a specific view:

```python
from pydantic import ValidationError


def signup(request):
    try:
        data = SignupSchema(request)
    except ValidationError as exc:
        errors = {e["loc"][0]: e["msg"] for e in exc.errors(include_url=False)}
        return JsonResponse({"errors": errors}, status=400)

    return JsonResponse({"ok": True})
```

## License

This project is licensed under the terms of the [MIT license](LICENSE).
