from app.models.user import User, UserRole
from app.core.db import SessionLocal


class UserService:
    def __init__(self):
        self.db = SessionLocal()

    def create(self, email: str, first_name: str, last_name: str, grade: int, role: str = UserRole.USER) -> User:
        user = User(email=email, first_name=first_name, last_name=last_name, grade=grade, role=role)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def login(self, email: str) -> User:
        return self.db.query(User).filter(User.email == email).first()

    def get(self, user_id: str) -> User:
        return self.db.query(User).filter(User.id == user_id).first()

    def close(self):
        self.db.close()
