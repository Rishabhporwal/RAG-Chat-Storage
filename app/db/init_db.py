from app.db.base import Base
from app.db.session import engine
from app.db.models import *


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Tables created if not existing.")
