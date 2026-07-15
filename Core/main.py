from fastapi import FastAPI

from database import lifespan
import routers

app = FastAPI(title="CoreLedger API", lifespan=lifespan)

app.include_router(routers.transactions)