from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

class TransactionBase(BaseModel):
    amount: Decimal
    origin_device: str
    origin_app: str
    description: str
    category: str

class TransactionCreate(TransactionBase):
    account_id: UUID | None # If the account ID is provided, use as direct FK

class TransactionDB(TransactionBase):
    id: UUID
    created_at: datetime
    is_active: bool
    account_id: UUID # FK

class TransactionUpdate(BaseModel):
    id: Optional[UUID]
    description: Optional[str]
    category: Optional[str]  

class TransactionStaticQuery(BaseModel):
    id: Optional[UUID]
    is_active: Optional[bool]
    origin_device: Optional[str]
    origin_app: Optional[str]
    description: Optional[str]
    category: Optional[str]
    