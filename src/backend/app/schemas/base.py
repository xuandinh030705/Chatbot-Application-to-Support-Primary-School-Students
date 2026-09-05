from typing import Generic, TypeVar, Optional
from pydantic import BaseModel

T = TypeVar("T")


class BaseResponse(BaseModel, Generic[T]):
    code: Optional[int] = 200
    success: bool
    data: Optional[T] = None
    error: Optional[str] = None
