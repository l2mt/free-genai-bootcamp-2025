"""
Punto de entrada de la aplicación FastAPI.
Se inicializan las tablas de la base de datos y se configuran los routers.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.models import Base
from app.database import engine
from app.routers import api

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Language Learning Portal API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api.router, prefix="/api")
