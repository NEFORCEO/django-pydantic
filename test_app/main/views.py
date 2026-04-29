from uuid import uuid4

from django.http import HttpRequest

from django_pydantic import ModelResponse

from test_app.main.schema import HelloRequest, HelloResponse


def hello_view(request: HttpRequest) -> ModelResponse[HelloResponse]:
    data = HelloRequest(request)
    return ModelResponse(HelloResponse(id=uuid4(), message=f"Hello {data.name}"))