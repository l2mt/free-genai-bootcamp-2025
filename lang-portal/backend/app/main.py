"""
Punto de entrada de la aplicación FastAPI.
Se inicializan las tablas de la base de datos y se configuran los routers.
"""

from fastapi import FastAPI
from app.models import Base
from app.database import engine
from app.routers import api

# Crear las tablas definidas en los modelos (para desarrollo).
# En producción se recomienda utilizar migraciones.
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Language Learning Portal API")

# Incluir los endpoints definidos en el router, con un prefijo /api
app.include_router(api.router, prefix="/api")
