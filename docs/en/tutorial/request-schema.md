# Request Schema

This page explains how `RequestModel` works and what makes it different from a plain `pydantic.BaseModel`.

## What is RequestModel?

`RequestModel` is a `pydantic.BaseModel` subclass that overrides the instantiation mechanism to accept a Django `HttpRequest`:

```python
from django_pydantic import RequestModel

class UserSchema(RequestModel):
    username: str
    email: str
```

The two call styles are equivalent from Pydantic's perspective:

```python
# Standard Pydantic style — still works
data = UserSchema(username="alice", email="alice@example.com")

# New style — pass the request directly
data = UserSchema(request)
```

## How does it work?

`RequestModel` uses a custom **metaclass** that intercepts object creation. When you call `MySchema(request)`, Python calls `type(MySchema).__call__(MySchema, request)`. The metaclass detects that the first argument is a `HttpRequest`, extracts the data, and forwards it to Pydantic's normal `__init__`:

```python
# Simplified internals — you don't write this
class _RequestModelMeta(type(BaseModel)):
    def __call__(cls, *args, **kwargs):
        if args and isinstance(args[0], HttpRequest):
            data = extract_data(args[0], **kwargs)  # (1)!
            return super().__call__(**data)          # (2)!
        return super().__call__(*args, **kwargs)     # (3)!
```

1. Extract a flat `dict` from the request (see [Request Data Sources](request-data.md)).
2. Call Pydantic's normal `__init__` with the extracted dict. Full validation runs here.
3. Fall back to standard Pydantic instantiation when no request is passed.

!!! info "No private Pydantic APIs"
    The metaclass inherits from `type(pydantic.BaseModel)` — no private imports.
    This means it stays compatible across Pydantic v2 minor versions.

## Regular Pydantic still works

Because `RequestModel` is a proper `BaseModel` subclass, everything you know about Pydantic applies:

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
            raise ValueError("Free items must have stock > 0")
        return self
```

## Nesting schemas

Nested Pydantic models work for JSON bodies:

```python
from pydantic import BaseModel
from django_pydantic import RequestModel


class AddressModel(BaseModel):
    street: str
    city: str


class OrderSchema(RequestModel):
    product_id: int
    quantity: int
    address: AddressModel  # nested, populated from JSON body
```

```bash
curl -X POST /order/ \
     -H "Content-Type: application/json" \
     -d '{"product_id": 42, "quantity": 3, "address": {"street": "Main St", "city": "NYC"}}'
```

!!! warning "Nested models require JSON"
    Nested Pydantic models can only be populated from a JSON body. HTML form data
    is flat by nature and cannot represent nested structures.

## Schema reuse

One schema can be used in multiple views — it's just a class:

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

## model_dump and serialization

`RequestModel` inherits all serialization methods from `BaseModel`:

```python
data = UserSchema(request)

data.model_dump()          # → dict
data.model_dump_json()     # → JSON string
data.model_fields_set      # → set of fields that were explicitly provided
```

Next: [Request Data Sources →](request-data.md)
