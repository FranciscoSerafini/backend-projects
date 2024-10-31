from pydantic import BaseModel, EmailStr
from typing import Optional

# Creación de un cliente
class ClienteCreate(BaseModel):
    dni: int
    nombre: str
    apellido: str
    direccion: str
    correo: EmailStr
    celular: str  
    id_tipo: int

    class Config:
        from_attributes = True

# Actualizar cliente
class ClienteUpdate(BaseModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    direccion: Optional[str] = None
    correo: Optional[EmailStr] = None
    celular: Optional[str] = None  
    id_tipo: Optional[int] = None

    class Config:
        from_attributes = True

# Lectura de un cliente
class ClienteRead(BaseModel):
    dni: int
    nombre: str
    apellido: str
    direccion: str
    correo: EmailStr
    celular: str
    id_tipo: int

    class Config:
        from_attributes = True
