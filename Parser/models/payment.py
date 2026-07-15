from datetime import datetime

from pydantic import BaseModel

class Payment(BaseModel):
    bank: str
    title: str
    body: str
    timestamp: datetime