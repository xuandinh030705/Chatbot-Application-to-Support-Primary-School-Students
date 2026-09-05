from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import uuid
import os
from dotenv import load_dotenv
from app.api import api_router
from app.containers import Container
from app.schemas.base import BaseResponse
from app.utils import logger

load_dotenv()
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3111")
origins = [
    "http://localhost:4000",  # local vite
    "http://localhost:3111",  # local vite
    "http://127.0.0.1:3111",
    "http://127.0.0.1:3999",
    "https://cacciatore-ilse-nonrecessive.ngrok-free.app",  # ngrok FE
]

container = Container()
app = FastAPI()
app.container = container
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_request_id(request: Request, call_next):
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id

    for handler in logger.handlers:
        handler.addFilter(lambda record: setattr(record, "request_id", request_id) or True)

    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response


app.include_router(api_router, prefix="/api")

# uvicorn app.main:app --reload
# tasklist /FI "IMAGENAME eq python.exe"
# taskkill /PID 11780  /F

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host="0.0.0.0"
    )
