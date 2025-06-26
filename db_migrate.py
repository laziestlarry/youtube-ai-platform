import asyncio
import os
from app.backend.core.database import init_db

async def main():
    print("Starting database initialization/migration...")
    # Ensure DATABASE_URL is set in the environment for the Cloud Run Job
    if not os.getenv("DATABASE_URL"):
        raise ValueError("DATABASE_URL environment variable is not set.")
    await init_db()
    print("Database initialization/migration complete.")

if __name__ == "__main__":
    asyncio.run(main())