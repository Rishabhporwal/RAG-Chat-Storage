import sys
import asyncio

sys.path.append(".")

from app.db.init_db import init_db

if __name__ == "__main__":
    asyncio.run(init_db())
    print("Database Tables Created")
