from sqlalchemy import Column, String, Text, TIMESTAMP
from sqlalchemy.sql import func
from enum import Enum

from app.core.db import Base
from app.utils.generate_uuid import generate_uuid


class ChatRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class ConversationStatus(str, Enum):
    ACTIVE = "active"
    DELETED = "deleted"


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(String(45), primary_key=True, default=generate_uuid)
    user_id = Column(String(45), nullable=False)
    status = Column(String(20), nullable=False, default=ConversationStatus.ACTIVE.value)
    created_at = Column(TIMESTAMP, server_default=func.now())


class ChatHistory(Base):
    __tablename__ = "messages"

    id = Column(String(45), primary_key=True, default=generate_uuid)
    conversation_id = Column(String(45), nullable=False)
    role = Column(String(20), nullable=False, default=ChatRole.USER.value)
    content = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
