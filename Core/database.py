from contextlib import asynccontextmanager
from typing import AsyncGenerator
import asyncpg
from asyncpg.pool import PoolConnectionProxy
from fastapi import FastAPI
from env import settings

class Database:
    pool: asyncpg.Pool | None = None

db = Database()

@asynccontextmanager
async def lifespan(app: FastAPI):
    db_url = settings.DB_URL
    if not db_url:
        raise ValueError("FATAL: The variable DB_URL is not defined inside the .env")
    
    db.pool = await asyncpg.create_pool(db_url)
    print("🟢 Plumbing connected: PostgreSQL pool ready and waiting for queries")
    
    yield # 👉 AQUÍ LA API VIVE Y RECIBE PETICIONES HTTP
    
    if db.pool:
        await db.pool.close()
        print("🔴 All PostgreSQL connections safely closed")

async def get_db_connection() -> AsyncGenerator[PoolConnectionProxy, None]:
    """
    Acquire a pool connection and injects it in the endpoint
    Once finished, the connection is automatically terminated
    """
    if db.pool is None:
        raise RuntimeError("Database pool is not initialized")
    
    async with db.pool.acquire() as connection:
        yield connection