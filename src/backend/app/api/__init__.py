from fastapi import APIRouter
from app.api.v1 import chat_router, user_router

api_router = APIRouter()
api_router.include_router(chat_router, prefix="/v1", tags=["chat"])
api_router.include_router(user_router, prefix="/v1", tags=["user"])
