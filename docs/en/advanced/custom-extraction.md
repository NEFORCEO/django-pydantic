# Custom Data Extraction

By default, django-pydantic merges GET params, POST/JSON body, and URL kwargs. If you need different behaviour for a specific schema, you can override the extraction logic.

## Default extraction (reference)

```python
# django_pydantic/request.py — what runs by default
def extract_data(request: HttpRequest, **extra) -> dict:
    data = {}
    data.update(request.GET.dict())

    content_type = (getattr(request, "content_type", "") or "").lower()
    if "application/json" in content_type:
        body = json.loads(request.body)
        if isinstance(body, dict):
            data.update(body)
    elif request.method not in {"GET", "HEAD", "OPTIONS", "DELETE"}:
        data.update(request.POST.dict())

    data.update(extra)
    return data
```

## Override per-schema

Override `_extract` classmethod on your schema to replace the extraction logic entirely:

```python
import json
from django.http import HttpRequest
from django_pydantic import RequestModel


class JsonOnlySchema(RequestModel):
    """Accepts only JSON body — rejects form data and query params."""

    @classmethod
    def _extract(cls, request: HttpRequest, **extra) -> dict:
        content_type = (getattr(request, "content_type", "") or "").lower()
        if "application/json" not in content_type:
            from pydantic import ValidationError
            raise ValueError("This endpoint only accepts application/json")
        data = json.loads(request.body)
        data.update(extra)
        return data
```

!!! note "Override `_extract`, not `__init__`"
    The metaclass calls `cls._extract(request, **kwargs)` when it detects a `HttpRequest`.
    Override this classmethod to customise extraction while keeping the metaclass machinery.

## Add headers to the schema

Useful for API versioning or auth tokens passed via headers:

```python
class AuthenticatedSchema(RequestModel):

    @classmethod
    def _extract(cls, request: HttpRequest, **extra) -> dict:
        from django_pydantic.request import extract_data
        data = extract_data(request, **extra)
        # Inject headers as fields
        data["api_key"] = request.headers.get("X-API-Key", "")
        data["api_version"] = request.headers.get("X-API-Version", "v1")
        return data


class MyEndpointSchema(AuthenticatedSchema):
    api_key: str = Field(min_length=32)
    api_version: str = "v1"
    payload: str
```

## Multipart file handling

```python
from django_pydantic import RequestModel
from django_pydantic.request import extract_data


class UploadSchema(RequestModel):
    title: str
    description: str = ""
    # file is handled separately — don't put UploadedFile in Pydantic

    @classmethod
    def _extract(cls, request, **extra):
        data = extract_data(request, **extra)
        return data


def upload_view(request):
    data = UploadSchema(request)
    file = request.FILES.get("file")   # handle separately
    if not file:
        return JsonResponse({"error": "file required"}, status=400)
    # save file + data...
```

!!! warning
    Pydantic is not designed to validate file objects. Validate `request.FILES`
    manually after the schema passes.
