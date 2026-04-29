# Ошибки валидации

Когда данные запроса не проходят валидацию Pydantic, django-pydantic-client автоматически возвращает структурированный ответ **HTTP 422 Unprocessable Entity**. Эта страница объясняет формат ошибок и способы кастомизации.

## Как это работает

`PydanticValidationMiddleware` автоматически устанавливается через `AppConfig.ready()`. Он подключается к механизму `process_exception` Django:

1. Вьюха вызывает `MySchema(request)`.
2. Pydantic бросает `ValidationError`, если данные невалидны.
3. Middleware перехватывает исключение до обработчика ошибок 500.
4. Возвращается `JsonResponse({"detail": [...]}, status=422)`.

Код вьюхи **не выполняется после строки со схемой** при невалидных данных.

## Формат ответа об ошибке

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

| Ключ | Описание |
|------|---------|
| `type` | Идентификатор типа ошибки Pydantic |
| `loc` | Путь к полю, которое не прошло валидацию |
| `msg` | Человекочитаемое сообщение об ошибке |
| `input` | Переданное значение |
| `ctx` | Доп. контекст (значения ограничений и т.д.) |

## Все ошибки сразу

Pydantic валидирует все поля перед тем, как бросить исключение — ты получаешь **все ошибки в одном ответе**, а не только первую:

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

Идеально для фронтенда: один запрос — все сломанные поля.

## Вложенные поля

Для вложенных моделей `loc` — это путь:

```python
class AddressSchema(BaseModel):
    city: str
    zip_code: str = Field(pattern=r"^\d{6}$")

class OrderSchema(RequestModel):
    address: AddressSchema
```

```json
{
  "detail": [
    {
      "type": "string_pattern_mismatch",
      "loc":  ["address", "zip_code"],
      "msg":  "String should match pattern '^\\d{6}$'"
    }
  ]
}
```

## Обработка ошибок вручную (по желанию)

Если хочешь обрабатывать ошибки валидации сам — используй try/except:

```python
from pydantic import ValidationError
from django.http import JsonResponse

from .schema import SignupSchema


def signup(request):
    try:
        data = SignupSchema(request)
    except ValidationError as exc:
        # Кастомная обработка
        errors = {e["loc"][0]: e["msg"] for e in exc.errors(include_url=False)}
        return JsonResponse({"errors": errors}, status=400)

    # продолжаем...
    return JsonResponse({"ok": True})
```

!!! tip
    При самостоятельном перехвате `ValidationError` middleware для этой вьюхи обходится.

## Кастомные сообщения через Field

```python
from pydantic import Field
from django_pydantic import RequestModel


class SignupSchema(RequestModel):
    username: str = Field(
        min_length=3,
        max_length=32,
        description="3–32 символа, только буквы и цифры",
    )
    age: int = Field(ge=18, description="Должно быть не менее 18")
```

Pydantic генерирует читаемые сообщения для всех встроенных ограничений автоматически.

## Кастомные валидаторы

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
            raise ValueError("Username может содержать только буквы и цифры")
        return v.lower()
```

Далее: [Параметры URL →](url-params.md)
