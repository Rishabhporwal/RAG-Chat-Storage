from fastapi import FastAPI
from app.api.routes import chat_message, chat_session


def register_routes(app: FastAPI):
    app.include_router(chat_session)
    app.include_router(chat_message)
