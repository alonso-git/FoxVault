from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from asyncpg.pool import PoolConnectionProxy

from models.account import AccountCreate, AccountStaticQuery, AccountUpdate
from database import get_db_connection

from services import db_service

# Le pasamos el administrador del ciclo de vida a FastAPI
accounts = APIRouter(
    prefix="/accounts",
    tags=["Accounts CRUD Interface"]
)

@accounts.post("/", status_code=status.HTTP_201_CREATED)
async def create_account(account: AccountCreate, conn: PoolConnectionProxy = Depends(get_db_connection)):
    result = await db_service.new_account(account, conn)

    if result:
        return result
    else:
        raise HTTPException(500)

@accounts.post("/search")
async def search_account(account_query: AccountStaticQuery, conn: PoolConnectionProxy = Depends(get_db_connection)):
    return await db_service.get_accounts(account_query, conn)

@accounts.put("/{account_id}")
async def update_account(account_id: UUID, account_update: AccountUpdate, conn: PoolConnectionProxy = Depends(get_db_connection)):
    result = await db_service.update_account(account_id, account_update, conn)

    if result:
        return result
    else:
        raise HTTPException(404, "Account not found")

@accounts.delete("/{account_id}")
async def delete_account(account_id: UUID, conn: PoolConnectionProxy = Depends(get_db_connection)):
    result = await db_service.delete_account(account_id, conn)

    if result:
        return result
    else:
        raise HTTPException(404, "Account not found")