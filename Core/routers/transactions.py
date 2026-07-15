from fastapi import APIRouter, Depends
from asyncpg.pool import PoolConnectionProxy

from database import get_db_connection

# Le pasamos el administrador del ciclo de vida a FastAPI
transactions = APIRouter(
    prefix="/transactions",
    tags=["Transactions Ingester"]
)

@transactions.get("/")
async def health_check(conn: PoolConnectionProxy = Depends(get_db_connection)):
    version = await conn.fetchval("SELECT version();")
    return {"status": "ok", "db_version": version}