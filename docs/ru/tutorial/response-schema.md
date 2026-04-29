# Схема ответа

Так же как `RequestModel` валидирует **входящие** данные, `ModelResponse` позволяет валидировать и сериализовать **исходящие**.

## Определи схему ответа

```python title="myapp/schema.py"
from uuid import UUID

from django_pydantic import RequestModel


class HelloRequest(RequestModel):
    name: str


class HelloResponse(RequestModel):
    id: UUID
    message: str
```

`RequestModel` — это обычная Pydantic `BaseModel`, поэтому её можно использовать и для ответов: типы полей, валидаторы и сериализация работают так же.

## Верни ModelResponse из вьюхи

```python title="myapp/views.py"
from uuid import uuid4

from django.http import HttpRequest

from django_pydantic import ModelResponse

from .schema import HelloRequest, HelloResponse


def hello(request: HttpRequest) -> ModelResponse[HelloResponse]:
    data = HelloRequest(request)
    return ModelResponse(
        HelloResponse(id=uuid4(), message=f"Привет, {data.name}!")
    )
```

`ModelResponse` оборачивает экземпляр Pydantic-модели в JSON-ответ. Типовой параметр `ModelResponse[HelloResponse]` даёт type checker'у всю необходимую информацию.

## Что ты получаешь

- **Сериализация через Pydantic** — `UUID`, `datetime`, `Decimal`, кастомные типы сериализуются корректно через `model_dump_json()`.
- **Типобезопасный возврат** — `ModelResponse[HelloResponse]` делает тип ответа явным. IDE автодополняет поля.
- **Валидация при создании** — `HelloResponse(...)` валидирует данные до того, как они попадут в ответ: невалидные исходящие данные вызывают ошибку сразу.

## Формат ответа

```bash
curl "http://localhost:8000/hello/?name=Алиса"
```

```json
{
  "id": "a1b2c3d4-...",
  "message": "Привет, Алиса!"
}
```

## Опционально: статус-код

```python
return ModelResponse(HelloResponse(...), status=201)
```

## Сравнение с JsonResponse

| | `JsonResponse(dict)` | `ModelResponse(schema)` |
|---|---|---|
| Типобезопасность | Нет | Да |
| UUID / datetime / Decimal | Через `DjangoJSONEncoder` | Через Pydantic |
| Валидация исходящих | Нет | Да |
| Автодополнение в IDE | Нет | Да |

Далее: [Параметры URL →](url-params.md)
