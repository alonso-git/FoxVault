from fastapi import FastAPI

import routers

app = FastAPI(redoc_url=None)

app.include_router(routers.webhook)