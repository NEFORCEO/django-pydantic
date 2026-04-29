# Request Data Sources

When you call `MySchema(request)`, django-pydantic-client builds a flat `dict` by merging data from multiple sources. This page explains exactly what gets merged and in what order.

## Merge order

Sources are merged left-to-right. **Later sources override earlier ones**.

```
GET params  →  POST / JSON body  →  URL kwargs (explicit)
  lowest                                   highest
  priority                                 priority
```

| Source | When used | Example |
|--------|-----------|---------|
| `request.GET` | Always | `?page=2&sort=name` |
| `request.POST` | Non-GET/HEAD/DELETE, non-JSON | HTML form submit |
| JSON body | `Content-Type: application/json` | REST API clients |
| URL kwargs | When passed explicitly | `MySchema(request, pk=pk)` |

!!! note
    POST form data and JSON body are **mutually exclusive** — only one is used depending
    on the `Content-Type` header.

## GET query parameters

Always included, regardless of HTTP method:

```python
class SearchSchema(RequestModel):
    q: str
    page: int = 1
    page_size: int = Field(default=20, le=100)
```

```
GET /search/?q=python&page=2
```

```python
data = SearchSchema(request)
# data.q        == "python"
# data.page     == 2
# data.page_size == 20  (default)
```

!!! tip "Type coercion"
    Query params arrive as strings. Pydantic coerces them to the declared type
    automatically — `"2"` becomes `int(2)`, `"true"` becomes `True`, etc.

## JSON body

Used when the request carries `Content-Type: application/json`:

```python
class CreateUserSchema(RequestModel):
    username: str
    email: EmailStr
    is_admin: bool = False
```

```bash
curl -X POST /users/ \
     -H "Content-Type: application/json" \
     -d '{"username": "alice", "email": "alice@example.com"}'
```

```python
data = CreateUserSchema(request)
# data.username == "alice"
# data.email    == "alice@example.com"
# data.is_admin == False
```

## POST form data

Used for standard HTML form submissions (`Content-Type: application/x-www-form-urlencoded` or `multipart/form-data`):

```html
<form method="POST" action="/contact/">
  <input name="name" type="text">
  <input name="email" type="email">
  <textarea name="message"></textarea>
</form>
```

```python
class ContactSchema(RequestModel):
    name: str
    email: EmailStr
    message: str = Field(min_length=10)


def contact(request):
    if request.method == "POST":
        data = ContactSchema(request)
        # send email...
```

## Mixing GET + body

GET params and body data are merged. This is useful for filtering endpoints that accept both URL-level pagination and body-level filter criteria:

```python
class ProductFilterSchema(RequestModel):
    page: int = 1          # from GET: /products/?page=3
    category: str = ""     # from JSON body or GET
    min_price: float = 0
    max_price: float = 99999
```

```
POST /products/?page=3
Content-Type: application/json

{"category": "electronics", "min_price": 100}
```

```python
data = ProductFilterSchema(request)
# data.page      == 3         (from GET)
# data.category  == "electronics"  (from JSON body)
# data.min_price == 100.0
```

## URL path parameters

URL kwargs are the highest priority source. Pass them explicitly:

```python
# urls.py
path("users/<int:pk>/", user_detail)

# views.py
def user_detail(request, pk):
    data = UserDetailSchema(request, pk=pk)  # (1)!
```

1. `pk` is merged into the data dict with highest priority, overriding any `pk` that might appear in the query string or body.

See [URL Parameters](url-params.md) for more details.

## Priority example

If the same key appears in multiple sources, the highest-priority source wins:

```
POST /items/?id=1
Content-Type: application/json

{"id": 2}
```

```python
class ItemSchema(RequestModel):
    id: int

# Called as: ItemSchema(request)
# GET says id=1, JSON body says id=2 → body wins → data.id == 2

# Called as: ItemSchema(request, id=99)
# URL kwarg wins → data.id == 99
```

Next: [Validation Errors →](validation.md)
