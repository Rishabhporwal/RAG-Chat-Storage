from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.api.routes import register_routes
from app.core.config import settings
from app.core.logging import setup_logging
from app.core.security import api_key_auth
from app.core.rate_limiter import limiter

setup_logging()

app = FastAPI(
    title="Rag Chat Storage Microservice",
    description="API's for Storing chat sessions and messages with context",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ["https://frontend-domain.com","http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)

register_routes(app)


@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok"}
