from sqlalchemy import Column, String, SmallInteger, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy import Enum as SAEnum
from enum import Enum

from app.core.db import Base
from app.utils.generate_uuid import generate_uuid


class UserRole(str, Enum):
    USER = "USER"
    PARENT = "PARENT"
    ADMIN = "ADMIN"


class User(Base):
    __tablename__ = "users"

    id = Column(String(45), primary_key=True, default=generate_uuid)
    email = Column(String(255), unique=True, nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    role = Column(SAEnum(UserRole), nullable=False)
    grade = Column(SmallInteger, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
