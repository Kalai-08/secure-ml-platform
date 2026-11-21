from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import app.models
from app.core.config import settings
from app.core.database import engine, Base
from app.routes import auth

Base.metadata.create_all(bind=engine) #bind means that the metadata will be created in the database specified by the engine

app = FastAPI(title="Secure ML Prediction Platform")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGIN,
    allow_credentials=True,
    allow_methods=["GET","POST"],
    allow_headers=["Authorization","Content-Type"]
)

app.include_router(auth.router)

@app.get("/health")
def health():
    return {"status": "ok"}