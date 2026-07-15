from fastapi import APIRouter

from models import Payment
from env import settings

webhook = APIRouter(
    prefix=f"{settings.API_URL}/payments",
    tags=["Payments Webhook"]
)

@webhook.post("/webhook/")
def notification_interceptor(payload: Payment):
    print(f"Notificacion recibida: {payload}")

    return {"status":"success", "action":"proccessed"}