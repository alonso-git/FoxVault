from decimal import Decimal, InvalidOperation

from fastapi import APIRouter, HTTPException
from services import regex, connectors

from models import RawTransaction, TransactionCreate
from env import settings

webhook = APIRouter(
    prefix=f"{settings.API_URL}/payments",
    tags=["Payments Webhook"]
)

@webhook.post("/webhook/")
async def notification_interceptor(payload: RawTransaction):
    print(f"Notificacion recibida: {payload}")
    amount: Decimal = Decimal()
    try:
        amount = regex.get_transaction_amount(payload.body)
        print(f"{amount}")
    except ValueError as e:
        raise HTTPException(422, e.args)
    except InvalidOperation as e:
        raise HTTPException(422, e.args)

    transaction = TransactionCreate(
        amount=amount,
        origin_app=payload.origin_app,
        origin_device=payload.origin_device,
        description=payload.body,
        category="",
        account_id=None
    )

    await connectors.core_store_transaction(transaction)

    return {"status":"success", "action":"proccessed"}