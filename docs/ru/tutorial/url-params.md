# Параметры URL

Path-параметры, которые Django URL-диспетчер передаёт в функцию, можно включить в схему — просто передай их как keyword-аргументы.

## Базовое использование

```python title="urls.py"
from django.urls import path
from .views import user_detail, user_update

urlpatterns = [
    path("users/<int:pk>/",       user_detail),
    path("users/<int:pk>/edit/",  user_update),
]
```

```python title="views.py"
from .schema import UserDetailSchema, UserUpdateSchema


def user_detail(request, pk):
    data = UserDetailSchema(request, pk=pk)   # (1)!
    user = User.objects.get(pk=data.pk)
    ...


def user_update(request, pk):
    data = UserUpdateSchema(request, pk=pk)
    User.objects.filter(pk=data.pk).update(**data.model_dump(exclude={"pk"}))
    ...
```

1. `pk` объединяется в словарь данных с **наивысшим приоритетом** — его нельзя переопределить через query string или тело запроса.

## Объявление path-параметров в схеме

Объявляй URL-параметры как обычные поля — они заполнятся из kwargs, которые ты передашь:

```python title="schema.py"
from pydantic import Field
from django_pydantic import RequestModel


class UserDetailSchema(RequestModel):
    pk: int = Field(gt=0)


class UserUpdateSchema(RequestModel):
    pk: int = Field(gt=0)
    username: str = Field(min_length=3, max_length=32)
    bio: str = ""
```

## Несколько URL-параметров

```python title="urls.py"
path("orgs/<int:org_id>/repos/<str:repo_slug>/", repo_detail),
```

```python title="views.py"
def repo_detail(request, org_id, repo_slug):
    data = RepoSchema(request, org_id=org_id, repo_slug=repo_slug)
    ...
```

```python title="schema.py"
class RepoSchema(RequestModel):
    org_id: int
    repo_slug: str
    # Плюс любые query/body-параметры:
    ref: str = "main"   # например ?ref=develop
```

## URL-параметры всегда побеждают

URL-kwargs выигрывают у query string и тела:

```python
path("items/<int:id>/", item_detail),
```

```
GET /items/42/?id=999
```

```python
def item_detail(request, id):
    data = ItemSchema(request, id=id)
    # data.id == 42, НЕ 999
    # URL kwarg имеет наивысший приоритет
```

!!! warning "Не забывай передавать kwargs"
    Если забудешь передать `id=id`, django-pydantic-client возьмёт `id` из query string
    (`?id=999`) — а это может быть не то, что нужно.
    Всегда передавай path-параметры явно.

## Slug-параметры

Django часто использует поля типа `slug`. Аннотируй их как `str` с regex-ограничением:

```python
from pydantic import Field
from django_pydantic import RequestModel


class ArticleSchema(RequestModel):
    slug: str = Field(pattern=r"^[a-z0-9-]+$")
```

```python
path("articles/<slug:slug>/", article_detail),

def article_detail(request, slug):
    data = ArticleSchema(request, slug=slug)
    article = Article.objects.get(slug=data.slug)
    ...
```

Далее: [Возможности Pydantic →](pydantic-features.md)
