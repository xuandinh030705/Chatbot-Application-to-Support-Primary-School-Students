from dependency_injector import containers, providers
from app.services.user_service import UserService
from app.services.chat_service import ChatService


class Container(containers.DeclarativeContainer):
    user_service = providers.Singleton(UserService)
    chat_service = providers.Singleton(
        ChatService,
        user_service=user_service
    )
