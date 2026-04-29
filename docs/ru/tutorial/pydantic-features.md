# Возможности Pydantic

`RequestModel` — полноценный подкласс `pydantic.BaseModel`. Все возможности Pydantic v2 работают без изменений.

## Ограничения через Field

```python
from pydantic import Field, EmailStr
from django_pydantic import RequestModel


class SignupSchema(RequestModel):
    username: str    = Field(min_length=3, max_length=32, pattern=r"^[a-zA-Z0-9_]+$")
    email: EmailStr
    password: str    = Field(min_length=8)
    age: int         = Field(ge=18, le=120)
    website: str     = Field(default="", max_length=200)
```

## Необязательные поля и значения по умолчанию

```python
from typing import Optional
from pydantic import Field
from django_pydantic import RequestModel


class ArticleFilterSchema(RequestModel):
    q: str               = ""           # пустая строка по умолчанию
    published: bool      = True
    author_id: Optional[int] = None     # None если не передан
    page: int            = Field(default=1, ge=1)
    page_size: int       = Field(default=20, ge=1, le=100)
```

!!! tip
    Поля со значением по умолчанию никогда не обязательны. Запрос может их не передавать вообще.

## Алиасы полей

Используй `alias`, когда имя поля в запросе отличается от Python-атрибута:

```python
from pydantic import Field
from django_pydantic import RequestModel


class SearchSchema(RequestModel):
    query: str    = Field(alias="q")       # запрос отправляет ?q=python
    per_page: int = Field(default=20, alias="per_page")

    model_config = {"populate_by_name": True}
```

```
GET /search/?q=python
```

```python
data = SearchSchema(request)
# data.query == "python"
```

## Валидаторы полей

```python
from pydantic import field_validator
from django_pydantic import RequestModel


class TagSchema(RequestModel):
    tags: str  # через запятую: "python,django,pydantic"

    @field_validator("tags")
    @classmethod
    def parse_tags(cls, v: str) -> list[str]:
        return [t.strip() for t in v.split(",") if t.strip()]
```

```
POST /articles/
{"tags": "python, django, pydantic"}
```

```python
data = TagSchema(request)
# data.tags == ["python", "django", "pydantic"]
```

## Валидаторы модели

```python
from pydantic import model_validator
from django_pydantic import RequestModel


class DateRangeSchema(RequestModel):
    date_from: str
    date_to: str

    @model_validator(mode="after")
    def check_dates(self):
        if self.date_from > self.date_to:
            raise ValueError("date_from должен быть раньше date_to")
        return self
```

## Вычисляемые поля

```python
from pydantic import computed_field, Field
from django_pydantic import RequestModel


class PaginationSchema(RequestModel):
    page: int      = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)

    @computed_field
    @property
    def offset(self) -> int:
        return (self.page - 1) * self.page_size
```

```python
data = PaginationSchema(request)
qs = MyModel.objects.all()[data.offset : data.offset + data.page_size]
```

## model_config

```python
from pydantic import ConfigDict
from django_pydantic import RequestModel


class StrictSchema(RequestModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,  # убирает пробелы по краям
        str_to_lower=True,          # lowercase все строки
        extra="forbid",             # запрещает неизвестные поля
    )

    username: str
    email: str
```

## Аннотированные типы

```python
from typing import Annotated
from pydantic import Field
from django_pydantic import RequestModel


PositiveInt = Annotated[int, Field(gt=0)]
ShortStr    = Annotated[str, Field(max_length=100)]


class ProductSchema(RequestModel):
    name: ShortStr
    price: float = Field(gt=0)
    stock: PositiveInt = 0
```

## Сериализация через model_dump

После валидации доступны все стандартные методы Pydantic:

```python
def create_user(request):
    data = SignupSchema(request)

    # Сохранить в БД — исключить поля, которых нет в модели
    User.objects.create(**data.model_dump(exclude={"confirm_password"}))

    # Вернуть ответ
    return JsonResponse(data.model_dump(exclude={"password"}))
```
