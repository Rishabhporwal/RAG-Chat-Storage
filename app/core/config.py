from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    API_KEY: str = "super-secret-key"
    DATABASE_URL: str = "postgresql://postgres:postgres@db:5432/rag_chat"

    class Config:
        env_file = ".env"


settings = Settings()
