from fastapi import APIRouter, Depends
from asyncpg.pool import PoolConnectionProxy

from database import get_db_connection

from services import db_admin

# Le pasamos el administrador del ciclo de vida a FastAPI
db = APIRouter(
    prefix="/database",
    tags=["Database Admin (if you see this, go ahead and drop the DB. Either it does not matter or I deserve it for allowing it)"]
)

@db.get("/create")
async def create_database(conn: PoolConnectionProxy = Depends(get_db_connection)):
    await db_admin.reset_db(conn)

@db.get("/")
async def health_check(conn: PoolConnectionProxy = Depends(get_db_connection)):
    version = await conn.fetchval("SELECT version();")
    accountTypes = await conn.fetch("SELECT * FROM AccountTypes;")
    accounts = await conn.fetch("SELECT * FROM Accounts;")
    transactions = await conn.fetch("SELECT * FROM Transactions;")
    print(accountTypes)
    print(accounts)
    print(transactions)
    return {"status": "ok", "db_version": version}