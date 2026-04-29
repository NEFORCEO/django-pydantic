# Вьюхи на классах

`RequestModel` работает с Django class-based views без дополнительной настройки.

## View-класс

```python
from django.views import View
from django.http import JsonResponse

from .schema import ArticleCreateSchema


class ArticleView(View):

    def get(self, request):
        from .schema import ArticleListSchema
        params = ArticleListSchema(request)
        articles = Article.objects.filter(
            published=params.published,
        )[params.offset : params.offset + params.page_size]
        return JsonResponse({"results": list(articles.values())})

    def post(self, request):
        data = ArticleCreateSchema(request)
        article = Article.objects.create(
            title=data.title,
            body=data.body,
            author=request.user,
        )
        return JsonResponse({"id": article.pk}, status=201)
```

## Detail-вьюха с URL-параметром

```python
class ArticleDetailView(View):

    def get(self, request, pk):
        data = ArticleDetailSchema(request, pk=pk)
        article = Article.objects.get(pk=data.pk)
        return JsonResponse({"title": article.title})

    def patch(self, request, pk):
        data = ArticleUpdateSchema(request, pk=pk)
        Article.objects.filter(pk=data.pk).update(
            **data.model_dump(exclude={"pk"}, exclude_unset=True)
        )
        return JsonResponse({"ok": True})

    def delete(self, request, pk):
        Article.objects.filter(pk=pk).delete()
        return JsonResponse({}, status=204)
```

## LoginRequiredMixin + валидация

```python
from django.contrib.auth.mixins import LoginRequiredMixin


class ProfileUpdateView(LoginRequiredMixin, View):

    def post(self, request):
        data = ProfileUpdateSchema(request)
        request.user.profile.bio = data.bio
        request.user.profile.save()
        return JsonResponse({"ok": True})
```

## Django REST Framework APIView

Если используешь DRF, `RequestModel` тоже работает. DRF оборачивает `request.data`, но django-pydantic читает из оригинальных `request.body`/`request.POST`/`request.GET` — поэтому всё прозрачно:

```python
from rest_framework.views import APIView
from rest_framework.response import Response

from .schema import ProductCreateSchema


class ProductView(APIView):

    def post(self, request):
        data = ProductCreateSchema(request)  # читает из оригинального HttpRequest
        product = Product.objects.create(**data.model_dump())
        return Response({"id": product.pk}, status=201)
```

!!! note
    DRF-объект `request` оборачивает оригинальный `HttpRequest`. django-pydantic
    обращается к `request.body`, `request.GET` и `request.POST` — все они доступны
    и через DRF-обёртку.
