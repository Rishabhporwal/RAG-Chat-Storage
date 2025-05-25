from fastapi import FastAPI
from app.api.routes.chat_message import router as chat_message
from app.api.routes.chat_session import router as chat_session


def register_routes(app: FastAPI):
    app.include_router(chat_session)
    app.include_router(chat_message)
