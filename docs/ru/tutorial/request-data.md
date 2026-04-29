# Источники данных

При вызове `MySchema(request)` django-pydantic строит плоский `dict`, объединяя данные из нескольких источников. Эта страница объясняет, что именно объединяется и в каком порядке.

## Порядок слияния

Источники объединяются слева направо. **Более поздние источники перекрывают более ранние.**

```
GET-параметры  →  POST / JSON тело  →  URL kwargs (явные)
  низший                                   высший
  приоритет                                приоритет
```

| Источник | Когда используется | Пример |
|----------|-------------------|--------|
| `request.GET` | Всегда | `?page=2&sort=name` |
| `request.POST` | Не GET/HEAD/DELETE, не JSON | Отправка HTML-формы |
| JSON тело | `Content-Type: application/json` | REST API клиенты |
| URL kwargs | При явной передаче | `MySchema(request, pk=pk)` |

!!! note
    POST-данные формы и JSON-тело **взаимоисключающие** — используется только один
    источник в зависимости от заголовка `Content-Type`.

## GET-параметры запроса

Включаются всегда, независимо от HTTP-метода:

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
# data.page_size == 20  (по умолчанию)
```

!!! tip "Приведение типов"
    Параметры запроса приходят как строки. Pydantic автоматически приводит их
    к объявленному типу — `"2"` становится `int(2)`, `"true"` становится `True`.

## JSON-тело

Используется, когда запрос содержит `Content-Type: application/json`:

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

## POST-данные формы

Используются при стандартной отправке HTML-формы (`application/x-www-form-urlencoded` или `multipart/form-data`):

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
        # отправить email...
```

## Смешивание GET + тело

GET-параметры и данные тела объединяются. Удобно для фильтрующих эндпоинтов, которые принимают пагинацию через URL и критерии фильтрации через тело:

```python
class ProductFilterSchema(RequestModel):
    page: int = 1          # из GET: /products/?page=3
    category: str = ""     # из JSON или GET
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
# data.page      == 3               (из GET)
# data.category  == "electronics"   (из JSON)
# data.min_price == 100.0
```

## Параметры URL-пути

URL-kwargs имеют наивысший приоритет. Передавай их явно:

```python
# urls.py
path("users/<int:pk>/", user_detail)

# views.py
def user_detail(request, pk):
    data = UserDetailSchema(request, pk=pk)  # (1)!
```

1. `pk` объединяется в словарь данных с наивысшим приоритетом, перекрывая любой `pk` в query string или теле.

Подробнее: [Параметры URL](url-params.md).

## Пример приоритета

Если один ключ встречается в нескольких источниках, побеждает источник с наивысшим приоритетом:

```
POST /items/?id=1
Content-Type: application/json

{"id": 2}
```

```python
class ItemSchema(RequestModel):
    id: int

# Вызов: ItemSchema(request)
# GET говорит id=1, JSON говорит id=2 → тело выигрывает → data.id == 2

# Вызов: ItemSchema(request, id=99)
# URL kwarg выигрывает → data.id == 99
```

Далее: [Ошибки валидации →](validation.md)
