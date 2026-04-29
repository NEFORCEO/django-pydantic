# Первые шаги

Создадим простейшую валидированную Django-вьюху шаг за шагом.

## Установка

```bash
pip install django-pydantic
```

## Добавь в INSTALLED_APPS

```python title="settings.py" hl_lines="4"
INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.auth",
    "django_pydantic",  # добавь это
    # твои приложения...
]
```

!!! success "Middleware устанавливается автоматически"
    В `MIDDLEWARE` ничего добавлять не нужно. `django_pydantic` сам подключает
    `PydanticValidationMiddleware` при запуске Django.

## Создай схему

Внутри своего Django-приложения создай `schema.py`:

```python title="myapp/schema.py"
from django_pydantic import RequestModel


class HelloSchema(RequestModel):
    name: str
```

`RequestModel` — это подкласс `pydantic.BaseModel` с одной доп. возможностью: принимает Django `HttpRequest` первым аргументом.

## Напиши вьюху

```python title="myapp/views.py"
from django.http import JsonResponse

from .schema import HelloSchema


def hello(request):
    data = HelloSchema(request)  # (1)!
    return JsonResponse({"message": f"Привет, {data.name}!"})
```

1.  Если `name` отсутствует или невалиден, Pydantic бросает `ValidationError`.
    Middleware перехватывает его и возвращает **HTTP 422** автоматически.
    Код вьюхи не выполняется при невалидных данных.

## Зарегистрируй URL

```python title="myapp/urls.py"
from django.urls import path

from .views import hello

urlpatterns = [
    path("hello/", hello),
]
```

## Проверь

=== "GET-запрос"

    ```bash
    curl "http://localhost:8000/hello/?name=Алиса"
    ```

    ```json
    {"message": "Привет, Алиса!"}
    ```

=== "POST JSON"

    ```bash
    curl -X POST http://localhost:8000/hello/ \
         -H "Content-Type: application/json" \
         -d '{"name": "Алиса"}'
    ```

    ```json
    {"message": "Привет, Алиса!"}
    ```

=== "POST форма"

    ```bash
    curl -X POST http://localhost:8000/hello/ \
         -d "name=Алиса"
    ```

    ```json
    {"message": "Привет, Алиса!"}
    ```

## Что происходит при ошибке

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
    Поле `loc` точно указывает клиенту, какое поле не прошло валидацию. Фронтенд
    может сразу подсветить нужное поле ввода — без дополнительного кода.

## Итог

```python
from django_pydantic import RequestModel

class MySchema(RequestModel):   # (1)!
    field: type

def my_view(request):
    data = MySchema(request)    # (2)!
    ...                         # (3)!
```

1. Наследуйся от `RequestModel` вместо `BaseModel`.
2. Передай `request` — данные извлекаются и валидируются автоматически.
3. Если код дошёл до этой строки — `data` гарантированно валиден и типизирован.

Далее: [Схема запроса →](request-schema.md) — как это работает изнутри.
