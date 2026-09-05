from datetime import datetime
from pydantic import BaseModel


class LoginRequest(BaseModel):
    email: str


class RegisterRequest(BaseModel):
    email: str
    first_name: str
    last_name: str
    grade: int


class UserResponse(BaseModel):
    id: str
    email: str
    first_name: str
    last_name: str
    role: str
    grade: int
    created_at: datetime

    class Config:
        from_attributes = True
