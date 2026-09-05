from fastapi import APIRouter, Query
from fastapi.responses import StreamingResponse

from app.containers import Container
from app.schemas.base import BaseResponse
from app.services.chat_service import ChatService
from app.schemas.chat import Model, AskRequest
from app.utils import logger

chat_router = APIRouter(prefix="/chat", tags=["chat"])
container = Container()
chat_service: ChatService = container.chat_service()


@chat_router.get("/health", tags=["health"])
def health_check():
    try:
        return BaseResponse(
            success=True,
            data={"status": "ok"}
        )
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return BaseResponse(
            success=False,
            error=str(e)
        )


@chat_router.get(path="/user/{user_id}")
def get_conversation(user_id: str):
    try:
        logger.info("Get messages endpoint called with conversation id %s", user_id)
        result = chat_service.get_conversation(user_id=user_id)
        return BaseResponse(
            success=True,
            data=result
        )
    except Exception as e:
        logger.error(e)
        return BaseResponse(
            success=False,
            error=str(e)
        )


@chat_router.post("/ask")
async def ask(req: AskRequest):
    logger.info(f"Received request: sender_id={req.sender_id}, content={req.content}")

    try:
        response = chat_service.ask(
            sender_id=req.sender_id,
            content=req.content
        )
        logger.info(f"Ask response object: {response}")
        return BaseResponse(
            code=200,
            success=True,
            data=response
        )
    except Exception as e:
        logger.exception("Error while processing /ask request")
        return BaseResponse(
            success=False,
            error=str(e)
        )


@chat_router.get("/ask-stream")
async def ask_stream(
        sender_id: str = Query(...),
        content: str = Query(...),
        model: str = Query("gptoss120b")
):
    try:
        model = Model(model)
    except ValueError:
        model = Model.gptoss120b

    async def event_generator():
        try:
            for chunk in chat_service.ask(
                    sender_id=sender_id,
                    content=content,
                    model=model
            ):
                yield f"data: {chunk}\n\n"
            yield "data: [DONE]\n\n"
        except Exception as e:
            logger.error(f"Error streaming response: {e}")
            yield f"data: [ERROR] {str(e)}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")
