from fastapi import FastAPI
from routes.v1.qr import router as qr_router

app = FastAPI()

app.include_router(qr_router)