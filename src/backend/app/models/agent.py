from pydantic import BaseModel
from typing import List, Optional
from app.schemas.chat import Message, Model
from app.models.user import UserRole


class AgentInput(BaseModel):
    model: Optional[Model] = None
    stream: bool = True
    query: str
    role: UserRole
    user_name: str
    grade: int
    history: List[Message]
