from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel

class RawTransaction(BaseModel):
    origin_app: str
    origin_device: str
    title: str
    body: str
    timestamp: datetime

class TransactionBase(BaseModel):
    amount: Decimal
    origin_device: str
    origin_app: str
    description: str
    category: str

class TransactionCreate(TransactionBase):
    account_id: UUID | None # If the account ID is provided, use as direct FK