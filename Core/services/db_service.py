from enum import Enum
import types
from typing import Any, Union, get_args, get_origin
from uuid import UUID

from asyncpg.pool import PoolConnectionProxy
from asyncpg import Record, ForeignKeyViolationError
from pydantic import BaseModel

from models import AccountCreate, AccountStaticQuery, AccountUpdate, TransactionCreate, TransactionStaticQuery, TransactionUpdate

class ExistentTables(Enum):
    # Strict whitelist of tables to prevent SQL Injection
    ACCOUNT_TYPES = " AccountTypes"
    ACCOUNTS = "Accounts"
    TRANSACTIONS = "Transactions"


async def new_account(account: AccountCreate, conn: PoolConnectionProxy) -> Record | None:
    query = """
    INSERT INTO Accounts (
        institution,
        alias,
        type,
        balance
    ) VALUES (
        $1, $2, $3, $4
    ) RETURNING id, institution, alias, balance;
    """
    
    # Top hierarchy entity, insert worry-free
    result: Record | None = await conn.fetchrow(query, account.institution, account.alias, account.type, account.balance)

    return result

async def new_transaction(transaction: TransactionCreate, conn: PoolConnectionProxy) -> Record | None:
    query = """
    INSERT INTO Transactions (
        amount,
        origin_device,
        origin_app,
        description,
        category,
        account_id
    ) Values (
        $1, $2, $3, $4, $5, $6
    ) RETURNING id, amount, origin_device, origin_app, description;
    """

    # If account ID is not provided, search for it among DB recorded Accounts using app name (which should match "institution")
    account_id: UUID | None = transaction.account_id if transaction.account_id else await get_account_id_by_institution(transaction.origin_app, conn)

    # Note: Account ID provided by user (as argument) is not guaranteed to exist and its existance will skip DB search.
    # Do not trust the value on any process inside this function

    if account_id is not None:
        try: 
            result: Record | None = await conn.fetchrow(query, transaction.amount, transaction.origin_device, transaction.origin_app, transaction.description, transaction.category, account_id)
            return result
        except ForeignKeyViolationError:
            raise ForeignKeyViolationError
        
    return None

async def get_account_id_by_institution(institution: str, conn: PoolConnectionProxy) -> UUID | None:
    account_query = """
    SELECT a.id FROM Accounts AS a
    WHERE a.institution ILIKE '%' || $1 || '%';
    """

    # TODO: Fix this query to prevent several accounts of the same institution to be matched
    result = await conn.fetchval(account_query, institution)
    # Exception asyncpg.exceptions.TooManyRowsError will be thrown if that happens

    return result
    
async def get_accounts(account_query: AccountStaticQuery, conn: PoolConnectionProxy) -> list[Record]:
    print("PERO SI O PURA CACA")
    return await get_from_query_params(ExistentTables.ACCOUNTS, account_query, conn)

async def get_transactions(transactions_query: TransactionStaticQuery, conn: PoolConnectionProxy) -> list[Record]:
    return await get_from_query_params(ExistentTables.TRANSACTIONS, transactions_query, conn)

async def get_from_query_params(table: ExistentTables, query_model: BaseModel, conn: PoolConnectionProxy) -> list[Record]:
    clauses, variables = build_clauses_and_variable_list(query_model, include_id=True)
    
    if not clauses:
        return []
    else:
        query = f"SELECT a.* FROM {table.value} AS a WHERE " + clauses + f" {active_clause()};"

        print(f"{query=}")

        result: list[Record] = await conn.fetch(query, *variables)

        return result

async def update_account(account_id: UUID, account: AccountUpdate, conn: PoolConnectionProxy) -> Record | None:
    clauses, variables = build_clauses_and_variable_list(account, update=True)

    if not clauses:
        return None
    else:
        variables.append(account_id)
        query = "UPDATE Accounts SET " + clauses + f" WHERE id = ${len(variables)} {active_clause()} RETURNING id, institution, alias, type;"

        result: Record = await conn.fetchrow(query, *variables)

        return result
    
async def update_transaction(transaction_id: UUID, transaction: TransactionUpdate, conn: PoolConnectionProxy) -> Record | None:
    clauses, variables = build_clauses_and_variable_list(transaction, update=True)

    if not clauses:
        return None
    else:
        variables.append(transaction_id)
        query = "UPDATE Transactions SET " + clauses + f"WHERE id = ${len(variables)} {active_clause()} RETURNING id, description, category;"

        result: Record = await conn.fetchrow(query, *variables)

        return result

async def delete_account(account_id: UUID, conn: PoolConnectionProxy) -> Record | None:
    return await delete_by_id(account_id, ExistentTables.ACCOUNTS, conn)

async def delete_transaction(transaction_id: UUID, conn: PoolConnectionProxy) -> Record | None:
    return await delete_by_id(transaction_id, ExistentTables.TRANSACTIONS, conn)

async def delete_by_id(row_id: UUID, table: ExistentTables, conn: PoolConnectionProxy) -> Record | None:
    query = f"UPDATE {table.value} SET is_active = FALSE WHERE id = $1 RETURNING *;"

    return await conn.fetchrow(query, row_id)

def active_clause(is_active: bool = True) -> str:
    """
    Returns  
    AND is_active = TRUE / FALSE  
    Depending on the parameter. Defaults to TRUE
    """
    return f"AND is_active = {'TRUE' if is_active else 'FALSE'}"

def build_clauses_and_variable_list(optional_model: BaseModel, defined_variables: int = 0, update: bool = False, include_id: bool = False) -> tuple[str, list[Any]]:
    """
    Builds a tuple of clauses (att_name = $n) and variables (n) to feed asyncpg positional variable system

    NOTE: Only nullable variables (var: type | None, var: Optional[None], var: Union[type, None]) on the model will be processed

    defined_variables must be defined with the number of previously defined $n variables in an asyncpg query
    If defined_variables > 0, you must provide the variables BEFORE the list this function returns

    update flag switches between UPDATE (", ") and SELECT (" AND ") syntax for joining the clauses

    include_id flag includes/excludes id attribute from provided models, in case you need to also query/modify them
    Its use paired with update=True must be reserved for very specific tasks, and usually is not recommended

    It will take model attributes' names and will be in the order they are defined on the class
    Using the asyncpg positional variables prevents SQL Injection, avoid direct string interpolation with user input
    """
    clauses: list[str] = []
    variables: list = []
    count = defined_variables

    for name, val in optional_model.model_dump(exclude={'' if include_id else 'id'}, exclude_unset=True).items():
        # Extract field metadata from class level (any Pydantic model can be processed this way)
        field_info = optional_model.__class__.model_fields[name]

        print(f"{name=} {val=} {field_info.annotation}")

        # Make sure it is a "strictly typed nullable" where only a type and None are allowed
        if is_nullable(field_info.annotation):
            print("ok")
            count += 1
            clauses.append(f"{name} = ${count}")
            variables.append(val)

    return ((", " if update else " AND ").join(clauses), variables)
    
def is_nullable(type_ann: Any | None) -> bool:
    """
    Accepted types:  
    Union[type, None],  Optional[type],  type | None
    """
    origin = get_origin(type_ann)
    if origin is Union or origin is getattr(types, "UnionType", None):
        args = get_args(type_ann)
        return type(None) in args and len(args) == 2
    else:
        return False