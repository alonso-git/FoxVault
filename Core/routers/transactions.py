from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from asyncpg.pool import PoolConnectionProxy

from models import TransactionCreate, TransactionStaticQuery, TransactionUpdate
from database import get_db_connection

from services import db_admin, db_service

# Le pasamos el administrador del ciclo de vida a FastAPI
transactions = APIRouter(
    prefix="/transactions",
    tags=["Transactions Ingester"]
)
@transactions.post("/", status_code=status.HTTP_201_CREATED)
async def create_transaction(transaction: TransactionCreate, conn: PoolConnectionProxy = Depends(get_db_connection)):
    print(f"{transaction=}")
    result = await db_service.new_transaction(transaction, conn)

    if result:          
        return result
    else:
        raise HTTPException(500)

@transactions.post("/search")
async def search_transaction(transaction_query: TransactionStaticQuery, conn: PoolConnectionProxy = Depends(get_db_connection)):
    return await db_service.get_transactions(transaction_query, conn)

@transactions.put("/{transaction_id}")
async def update_transaction(transaction_id: UUID, transaction_update: TransactionUpdate, conn: PoolConnectionProxy = Depends(get_db_connection)):
    result = await db_service.update_transaction(transaction_id, transaction_update, conn)

    if result:
        return result
    else:
        raise HTTPException(404, "Transaction not found")

@transactions.delete("/{transaction_id}")
async def delete_transaction(transaction_id: UUID, conn: PoolConnectionProxy = Depends(get_db_connection)):
    result = await db_service.delete_transaction(transaction_id, conn)

    if result:
        return result
    else:
        raise HTTPException(404, "Transaction not found")