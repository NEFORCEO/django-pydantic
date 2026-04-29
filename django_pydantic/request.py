import json

from django.http import HttpRequest


def extract_data(request: HttpRequest, **extra: object) -> dict:
    """Extract request data into a flat dict suitable for Pydantic validation.

    Merges sources in this order (later sources win):
    1. GET query parameters
    2. POST form fields or JSON body (depending on Content-Type)
    3. Extra keyword arguments (e.g. URL path parameters)

    Args:
        request: The incoming Django HttpRequest.
        **extra: Additional key-value pairs to merge into the result,
                 typically URL path parameters captured by the view.

    Returns:
        A flat dict with all extracted values ready for Pydantic model_validate.
    """
    data: dict = {}

    data.update(request.GET.dict())

    content_type = (getattr(request, "content_type", "") or "").lower()

    if "application/json" in content_type:
        try:
            body = json.loads(request.body)
            if isinstance(body, dict):
                data.update(body)
        except (json.JSONDecodeError, UnicodeDecodeError):
            pass
    elif request.method not in {"GET", "HEAD", "OPTIONS", "DELETE"}:
        data.update(request.POST.dict())

    data.update(extra)
    return data
