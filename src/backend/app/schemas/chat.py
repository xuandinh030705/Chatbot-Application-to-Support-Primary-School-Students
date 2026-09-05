from pydantic import BaseModel
from enum import Enum


class Message(BaseModel):
    id: str
    role: str
    content: str
    created_at: str


class Model(str, Enum):
    gpt4o = "gpt4o"
    gpt4omini = "gpt4omini"
    gptoss120b = "gptoss120b"
    gptoss20b = "gptoss20b"


class AskRequest(BaseModel):
    sender_id: str
    content: str


class AskResponse(BaseModel):
    question: Message
    answer: Message
