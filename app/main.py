from fastapi import FastAPI
from app.api.routes import register_routes
from app.core.config import settings
from app.db.init_db import init_db


app = FastAPI(
    title="Rag Chat Storage Microservice",
    description="Stores chat sessions and messgaes with context",
    version="1.0.0",
)

register_routes(app)


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}
