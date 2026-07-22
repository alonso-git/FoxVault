from fastapi import HTTPException
import httpx

from models import TransactionCreate
from env import settings

async def core_store_transaction(transaction: TransactionCreate):
    endpoint = f"{settings.CORE_URL}/transactions/"

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(endpoint, json=transaction.model_dump(mode='json'))

            response.raise_for_status()

            return response.json()
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code,
                detail=f"The Core service failed: {e.response.text}"
            )