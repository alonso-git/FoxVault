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
        raise ValueError("FATAL: La variable DB_URL no está definida en el .env")
    
    db.pool = await asyncpg.create_pool(db_url)
    print("🟢 Plomería conectada: Pool de PostgreSQL listo y esperando queries.")
    
    yield # 👉 AQUÍ LA API VIVE Y RECIBE PETICIONES HTTP
    
    if db.pool:
        await db.pool.close()
        print("🔴 Conexiones a PostgreSQL cerradas de forma segura.")

async def get_db_connection() -> AsyncGenerator[PoolConnectionProxy, None]:
    """
    Adquiere una conexión del pool y la inyecta en el endpoint.
    Al terminar el endpoint, la conexión se libera automáticamente.
    """
    if db.pool is None:
        raise RuntimeError("El pool de base de datos no está inicializado.")
    
    async with db.pool.acquire() as connection:
        yield connection