from app.db.base import Base
from app.db.session import engine
from app.db.models import *
from app.core.logging import logger


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Tables created if not existing.")
