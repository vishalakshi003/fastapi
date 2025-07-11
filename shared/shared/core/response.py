from typing import TypeVar, Generic, Optional
import strawberry

T = TypeVar("T")

@strawberry.type
class Response(Generic[T]):
    status: str  # "success" or "error"
    message: str
    status_code:int
    data: Optional[T] = None
