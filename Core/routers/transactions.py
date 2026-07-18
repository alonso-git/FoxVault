from fastapi import APIRouter, Depends
from asyncpg.pool import PoolConnectionProxy

from database import get_db_connection

from services import db_admin, db_service

# Le pasamos el administrador del ciclo de vida a FastAPI
transactions = APIRouter(
    prefix="/transactions",
    tags=["Transactions Ingester"]
)