# Схема запроса

Эта страница объясняет, как работает `RequestModel` и чем он отличается от обычного `pydantic.BaseModel`.

## Что такое RequestModel?

`RequestModel` — подкласс `pydantic.BaseModel`, который переопределяет механизм создания объектов, чтобы принимать Django `HttpRequest`:

```python
from django_pydantic import RequestModel

class UserSchema(RequestModel):
    username: str
    email: str
```

Оба стиля вызова равнозначны с точки зрения Pydantic:

```python
# Стандартный Pydantic — по-прежнему работает
data = UserSchema(username="alice", email="alice@example.com")

# Новый стиль — передаёшь request напрямую
data = UserSchema(request)
```

## Как это работает?

`RequestModel` использует кастомный **метакласс**, который перехватывает создание объекта. При вызове `MySchema(request)` Python вызывает `type(MySchema).__call__(MySchema, request)`. Метакласс определяет, что первый аргумент — `HttpRequest`, извлекает данные и передаёт их в стандартный `__init__` Pydantic:

```python
# Упрощённые внутренности — ты это не пишешь
class _RequestModelMeta(type(BaseModel)):
    def __call__(cls, *args, **kwargs):
        if args and isinstance(args[0], HttpRequest):
            data = extract_data(args[0], **kwargs)  # (1)!
            return super().__call__(**data)          # (2)!
        return super().__call__(*args, **kwargs)     # (3)!
```

1. Извлекаем плоский `dict` из запроса (см. [Источники данных](request-data.md)).
2. Вызываем стандартный `__init__` Pydantic с извлечёнными данными. Здесь запускается полная валидация.
3. Фолбэк на стандартное создание объекта Pydantic, когда request не передан.

!!! info "Никаких приватных API Pydantic"
    Метакласс наследуется от `type(pydantic.BaseModel)` — без приватных импортов.
    Совместимость сохраняется между минорными версиями Pydantic v2.

## Стандартный Pydantic работает как обычно

Поскольку `RequestModel` — правильный подкласс `BaseModel`, всё, что ты знаешь о Pydantic, применимо здесь:

```python
from pydantic import Field, model_validator
from django_pydantic import RequestModel


class ProductSchema(RequestModel):
    name: str = Field(min_length=1, max_length=100)
    price: float = Field(gt=0)
    quantity: int = Field(ge=0, default=0)

    @model_validator(mode="after")
    def check_stock(self):
        if self.quantity == 0 and self.price < 1.0:
            raise ValueError("Бесплатные товары должны иметь остаток > 0")
        return self
```

## Вложенные схемы

Вложенные Pydantic-модели работают для JSON-тела:

```python
from pydantic import BaseModel
from django_pydantic import RequestModel


class AddressModel(BaseModel):
    street: str
    city: str


class OrderSchema(RequestModel):
    product_id: int
    quantity: int
    address: AddressModel  # вложенная, заполняется из JSON
```

```bash
curl -X POST /order/ \
     -H "Content-Type: application/json" \
     -d '{"product_id": 42, "quantity": 3, "address": {"street": "Ленина 1", "city": "Москва"}}'
```

!!! warning "Вложенные модели требуют JSON"
    Вложенные Pydantic-модели можно заполнить только из JSON-тела. HTML-форма
    по природе своей плоская и не может представлять вложенные структуры.

## Переиспользование схем

Одна схема работает в нескольких вьюхах — это просто класс:

```python
class PaginationSchema(RequestModel):
    page: int = Field(ge=1, default=1)
    page_size: int = Field(ge=1, le=100, default=20)


def article_list(request):
    p = PaginationSchema(request)
    qs = Article.objects.all()[(p.page - 1) * p.page_size : p.page * p.page_size]
    ...


def comment_list(request):
    p = PaginationSchema(request)
    ...
```

## model_dump и сериализация

`RequestModel` наследует все методы сериализации от `BaseModel`:

```python
data = UserSchema(request)

data.model_dump()          # → dict
data.model_dump_json()     # → JSON-строка
data.model_fields_set      # → множество полей, которые были явно переданы
```

Далее: [Источники данных →](request-data.md)
