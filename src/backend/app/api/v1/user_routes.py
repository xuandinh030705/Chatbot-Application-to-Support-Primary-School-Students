from fastapi import APIRouter

from app.schemas.user import LoginRequest, UserResponse, RegisterRequest
from app.schemas.base import BaseResponse
from app.services.user_service import UserService
from app.containers import Container
from app.utils import logger

user_router = APIRouter(prefix="/user", tags=["user"])
container = Container()
user_service: UserService = container.user_service()


@user_router.post(
    path="/login",
    response_model=BaseResponse[UserResponse]
)
def login(req: LoginRequest):
    logger.info(f"Login request with email: {req.email}")
    user = user_service.login(req.email)
    if not user:
        logger.warning(f"Login failed, user not found: {req.email}")
        return BaseResponse(
            code=404,
            success=False,
            data=None,
            error=f"Login failed, user not found: {req.email}"
        )

    return BaseResponse(
        success=True,
        data=user
    )


@user_router.post(
    path="/register",
    response_model=BaseResponse[UserResponse]
)
def register(req: RegisterRequest):
    logger.info(f"Register request with email: {req.email}")

    # Kiểm tra user tồn tại
    existing_user = user_service.login(req.email)
    if existing_user:
        logger.warning(f"Register failed, email already exists: {req.email}")
        return BaseResponse(
            code=400,
            success=False,
            data=None,
            error=f"Register failed, email already exists: {req.email}"
        )

    # Tạo user mới
    user = user_service.create(
        email=req.email,
        first_name=req.first_name,
        last_name=req.last_name,
        grade=req.grade
    )

    logger.info(f"User registered successfully: {user.email}")
    return BaseResponse(
        success=True,
        data=user
    )
