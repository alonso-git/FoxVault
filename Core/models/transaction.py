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
    description: Optional[str] = None
    category: Optional[str] = None

class TransactionStaticQuery(TransactionUpdate):
    id: Optional[UUID] = None
    is_active: Optional[bool] = None
    origin_device: Optional[str] = None
    origin_app: Optional[str] = None
    