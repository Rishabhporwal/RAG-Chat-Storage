from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter
from slowapi.util import get_remote_address
from app.api.routes import register_routes
from app.core.config import settings
from app.core.logging import setup_logging
from app.core.security import api_key_auth
from app.core.rate_limiter import limiter

setup_logging()

app = FastAPI(
    title="Rag Chat Storage Microservice",
    description="Stores chat sessions and messgaes with context",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_routes(app)


@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok"}
