from fastapi import FastAPI
from routes.v1.qr import router as qr_router
from routes.v1.notes import router as notes_router

app = FastAPI()

app.include_router(qr_router)
app.include_router(notes_router)