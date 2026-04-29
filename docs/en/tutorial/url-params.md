# URL Parameters

URL path parameters captured by Django's URL dispatcher can be included in your schema by passing them as keyword arguments.

## Basic usage

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

1. `pk` is merged into the data dict with **highest priority** — it cannot be overridden by query params or request body.

## Defining path params in the schema

Declare URL params as regular fields. They'll be populated from the kwargs you pass:

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

## Multiple URL parameters

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
    # Plus any query/body params you want:
    ref: str = "main"   # e.g. ?ref=develop
```

## URL params override everything

URL kwargs always win over query string and body:

```python
path("items/<int:id>/", item_detail),
```

```
GET /items/42/?id=999
```

```python
def item_detail(request, id):
    data = ItemSchema(request, id=id)
    # data.id == 42, NOT 999
    # URL kwarg has highest priority
```

!!! warning "Don't skip the kwarg"
    If you forget to pass `id=id`, django-pydantic will pick up `id` from the
    query string (`?id=999`) instead — which may not be what you want.
    Always pass path parameters explicitly.

## Slug parameters

Django often uses `slug` fields. Annotate them as `str` with a regex constraint:

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

Next: [Pydantic Features →](pydantic-features.md)
