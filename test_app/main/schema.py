from uuid import UUID

from django_pydantic import RequestModel


class HelloRequest(RequestModel):
    name: str
    
    def __str__(self) -> str:
        return self.name
    

class HelloResponse(RequestModel):
    id: UUID
    message: str
    
    def __str__(self) -> str:
        return str(self.id)