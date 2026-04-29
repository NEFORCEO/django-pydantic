from __future__ import annotations

from pydantic import BaseModel

_PydanticMeta = type(BaseModel)


class _RequestModelMeta(_PydanticMeta):
    """Metaclass that intercepts instantiation with a Django HttpRequest.

    Allows ``MySchema(request)`` and ``MySchema(request, pk=pk)`` in addition
    to the standard Pydantic ``MySchema(field=value, ...)`` call style.
    """

    def __call__(cls, *args: object, **kwargs: object) -> object:
        from django.http import HttpRequest

        from .request import extract_data

        if args and isinstance(args[0], HttpRequest):
            data = extract_data(args[0], **kwargs)
            return super().__call__(**data)

        return super().__call__(*args, **kwargs)


class RequestModel(BaseModel, metaclass=_RequestModelMeta):
    """Pydantic BaseModel subclass that can be instantiated from a Django HttpRequest.

    Usage::

        class MySchema(RequestModel):
            name: str
            age: int

        def my_view(request):
            data = MySchema(request)         # validates GET/POST/JSON body
            ...

        def detail_view(request, pk):
            data = MySchema(request, pk=pk)  # URL kwargs merged in
            ...

    On validation failure ``pydantic.ValidationError`` is raised.
    ``PydanticValidationMiddleware`` converts it to a 422 JSON response automatically.
    """
