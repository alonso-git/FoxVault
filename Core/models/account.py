from datetime import datetime
from decimal import Decimal
from enum import IntEnum
from uuid import UUID

from pydantic import BaseModel, ConfigDict

class AccountType(IntEnum):
    DEBIT = 1
    CREDIT = 2
    INVEST = 3

class AccountBase(BaseModel):
    institution: str
    alias: str
    type: AccountType
    balance: Decimal

class AccountCreate(AccountBase):
    pass

class AccountDB(AccountCreate):
    id: UUID
    created_at: datetime
    updated_at: datetime
    is_active: bool

    model_config = ConfigDict(from_attributes=True)