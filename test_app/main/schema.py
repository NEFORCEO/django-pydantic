from uuid import UUID

from pydantic import BaseModel

from django_pydantic import RequestModel


class HelloRequest(RequestModel):
    name: str

    def __str__(self) -> str:
        return self.name


class HelloResponse(BaseModel):
    id: UUID
    message: str

    def __str__(self) -> str:
        return str(self.id)