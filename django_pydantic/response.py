from __future__ import annotations

from typing import Any, Generic, TypeVar

from django.http import JsonResponse
from pydantic import BaseModel

_M = TypeVar("_M", bound=BaseModel)


class ModelResponse(JsonResponse, Generic[_M]):
    def __init__(self, model: _M, status: int = 200, **kwargs: Any) -> None:
        super().__init__(
            model.model_dump(mode="json"),
            status=status,
            **kwargs,
        )
