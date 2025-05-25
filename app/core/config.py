from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

# Explicitly load the .env file
env_path = os.path.join(os.path.dirname(__file__), "..", "..", ".env")
load_dotenv(dotenv_path=env_path)


class Settings(BaseSettings):
    API_KEY: str
    DATABASE_URL: str
    REDIS_URL: str
    RATE_LIMIT: str = "10/Minute"
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"


settings = Settings()

print(f"📦 DATABASE_URL used: {settings.DATABASE_URL}")
