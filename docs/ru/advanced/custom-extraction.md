# Своя обработка данных

По умолчанию django-pydantic-client объединяет GET-параметры, POST/JSON тело и URL kwargs. Если для конкретной схемы нужно другое поведение — переопредели логику извлечения.

## Извлечение по умолчанию (справка)

```python
# django_pydantic/request.py — что запускается по умолчанию
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

## Переопределение для конкретной схемы

Переопредели classmethod `_extract`, чтобы полностью заменить логику извлечения:

```python
import json
from django.http import HttpRequest
from django_pydantic import RequestModel


class JsonOnlySchema(RequestModel):
    """Принимает только JSON — отклоняет форму и query-параметры."""

    @classmethod
    def _extract(cls, request: HttpRequest, **extra) -> dict:
        content_type = (getattr(request, "content_type", "") or "").lower()
        if "application/json" not in content_type:
            raise ValueError("Этот эндпоинт принимает только application/json")
        data = json.loads(request.body)
        data.update(extra)
        return data
```

!!! note "Переопределяй `_extract`, не `__init__`"
    Метакласс вызывает `cls._extract(request, **kwargs)`, когда обнаруживает `HttpRequest`.
    Переопредели этот classmethod для кастомизации, не трогая метакласс.

## Добавление заголовков в схему

Полезно для версионирования API или токенов авторизации, переданных через заголовки:

```python
class AuthenticatedSchema(RequestModel):

    @classmethod
    def _extract(cls, request: HttpRequest, **extra) -> dict:
        from django_pydantic.request import extract_data
        data = extract_data(request, **extra)
        # Инжектируем заголовки как поля
        data["api_key"] = request.headers.get("X-API-Key", "")
        data["api_version"] = request.headers.get("X-API-Version", "v1")
        return data


class MyEndpointSchema(AuthenticatedSchema):
    api_key: str = Field(min_length=32)
    api_version: str = "v1"
    payload: str
```

## Загрузка файлов (multipart)

```python
from django_pydantic import RequestModel
from django_pydantic.request import extract_data


class UploadSchema(RequestModel):
    title: str
    description: str = ""
    # файл обрабатывается отдельно — не помещай UploadedFile в Pydantic


def upload_view(request):
    data = UploadSchema(request)
    file = request.FILES.get("file")   # обрабатываем отдельно
    if not file:
        return JsonResponse({"error": "файл обязателен"}, status=400)
    # сохраняем файл + данные...
```

!!! warning
    Pydantic не предназначен для валидации файловых объектов. Валидируй `request.FILES`
    вручную после того, как схема прошла успешно.
