from __future__ import annotations

from typing import TYPE_CHECKING, Any, TypeVar, cast, overload

from pydantic import BaseModel

if TYPE_CHECKING:
    from django.http import HttpRequest

_PydanticMeta = type(BaseModel)
_T = TypeVar("_T")


class _RequestModelMeta(_PydanticMeta):
    def __call__(cls: type[_T], *args: object, **kwargs: object) -> _T:
        from django.http import HttpRequest

        from .request import extract_data

        if args and isinstance(args[0], HttpRequest):
            data = extract_data(args[0], **kwargs)
            return cast(_T, super().__call__(**data))

        return cast(_T, super().__call__(*args, **kwargs))


class RequestModel(BaseModel, metaclass=_RequestModelMeta):
    if TYPE_CHECKING:
        @overload
        def __init__(self, __request: HttpRequest, **path_kwargs: Any) -> None: ...
        @overload
        def __init__(self, **data: Any) -> None: ...
