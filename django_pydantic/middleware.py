from __future__ import annotations

from collections.abc import Callable

from django.http import HttpRequest, HttpResponse, JsonResponse
from pydantic import ValidationError


class PydanticValidationMiddleware:
    """Django middleware that converts ``pydantic.ValidationError`` to HTTP 422.

    Installed automatically when ``django_pydantic`` is in ``INSTALLED_APPS``.
    You do not need to add it manually to ``settings.MIDDLEWARE``.

    Response body on validation failure::

        {
            "detail": [
                {"loc": ["email"], "msg": "...", "type": "..."},
                ...
            ]
        }
    """

    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        return self.get_response(request)

    def process_exception(
        self, request: HttpRequest, exception: Exception
    ) -> HttpResponse | None:
        """Catch ValidationError and return a structured 422 response."""
        if isinstance(exception, ValidationError):
            return JsonResponse(
                {"detail": exception.errors(include_url=False)},
                status=422,
            )
        return None
