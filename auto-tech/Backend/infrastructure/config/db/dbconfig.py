from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Cadena de conexión (asegúrate de que sea para PostgreSQL async)
DATABASE_URL = "postgresql+asyncpg://postgres:@localhost:5432/"

# Crear el motor de la base de datos asíncrono
engine = create_async_engine(DATABASE_URL, echo=True)

# Crear la sesión asíncrona
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Crear la clase base
Base = declarative_base()

# Función de conexión a la base de datos
async def conexionDB():
    async with AsyncSessionLocal() as session:
        yield session  # Usar yield permite utilizarlo como una dependencia

