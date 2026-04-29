# Pydantic Features

`RequestModel` is a full `pydantic.BaseModel` subclass. Every Pydantic v2 feature works without any changes.

## Field constraints

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

## Optional fields and defaults

```python
from typing import Optional
from pydantic import Field
from django_pydantic import RequestModel


class ArticleFilterSchema(RequestModel):
    q: str               = ""           # empty string default
    published: bool      = True
    author_id: Optional[int] = None     # None if not provided
    page: int            = Field(default=1, ge=1)
    page_size: int       = Field(default=20, ge=1, le=100)
```

!!! tip
    Fields with defaults are never required. The request can omit them completely.

## Field aliases

Use `alias` when the request field name differs from your Python attribute name:

```python
from pydantic import Field
from django_pydantic import RequestModel


class SearchSchema(RequestModel):
    query: str  = Field(alias="q")       # request sends ?q=python
    per_page: int = Field(default=20, alias="per_page")

    model_config = {"populate_by_name": True}  # also allow .query = ...
```

```
GET /search/?q=python
```

```python
data = SearchSchema(request)
# data.query == "python"
```

## Field validators

```python
from pydantic import field_validator
from django_pydantic import RequestModel


class TagSchema(RequestModel):
    tags: str  # comma-separated: "python,django,pydantic"

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

## Model validators

```python
from pydantic import model_validator
from django_pydantic import RequestModel


class DateRangeSchema(RequestModel):
    date_from: str
    date_to: str

    @model_validator(mode="after")
    def check_dates(self):
        if self.date_from > self.date_to:
            raise ValueError("date_from must be before date_to")
        return self
```

## Computed fields

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
        str_strip_whitespace=True,  # strip leading/trailing spaces
        str_to_lower=True,          # lowercase all strings
        extra="forbid",             # reject unknown fields
    )

    username: str
    email: str
```

## Annotated types

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

## Serialization with model_dump

After validation, use all standard Pydantic serialization methods:

```python
def create_user(request):
    data = SignupSchema(request)

    # Save to DB — exclude fields not in the model
    User.objects.create(**data.model_dump(exclude={"confirm_password"}))

    # Return response
    return JsonResponse(data.model_dump(exclude={"password"}))
```
