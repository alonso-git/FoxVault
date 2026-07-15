from decimal import Decimal

import asyncpg
from asyncpg.pool import PoolConnectionProxy
from fastapi import Depends

from database import get_db_connection
from models import AccountCreate

async def new_account(account: AccountCreate, conn: PoolConnectionProxy = Depends(get_db_connection)):
    query = """
    INSERT INTO Accounts (
        institution,
        alias,
        type,
        balance
    ) VALUES (
        $1,$2,$3,$4
    ) RETURNING id, institution, alias, balance;
    """

    result = await conn.fetchrow(query, account.institution, account.alias, account.type, account.balance)

    return result