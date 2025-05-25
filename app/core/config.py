from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    API_KEY: str = "super-secret-key"
    DATABASE_URL: str = "postgresql://postgres:postgres@db:5432/rag_chat"
    REDIS_URL: str
    RATE_LIMIT: str = "100/Minute"
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"


settings = Settings()
