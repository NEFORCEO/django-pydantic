# Class-Based Views

`RequestModel` works with Django's class-based views without any special setup.

## View class

```python
from django.views import View
from django.http import JsonResponse

from .schema import ArticleCreateSchema, ArticleUpdateSchema


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

## Detail view with URL param

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

## LoginRequiredMixin + validation

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

If you use DRF, you can still use `RequestModel`. Note that DRF wraps `request.data`, but django-pydantic reads from the original `request.body`/`request.POST`/`request.GET` — so it works transparently:

```python
from rest_framework.views import APIView
from rest_framework.response import Response

from .schema import ProductCreateSchema


class ProductView(APIView):

    def post(self, request):
        data = ProductCreateSchema(request)  # reads from underlying HttpRequest
        product = Product.objects.create(**data.model_dump())
        return Response({"id": product.pk}, status=201)
```

!!! note
    The DRF `request` object wraps the original `HttpRequest`. django-pydantic's
    `extract_data` reads `request.body`, `request.GET`, and `request.POST` — all
    of which are accessible on the DRF wrapper as well.
