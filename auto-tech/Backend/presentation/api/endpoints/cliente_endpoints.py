from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from application.dtos.cliente_dtos import ClienteCreate, ClienteUpdate, ClienteRead
from application.services.cliente_service import ClienteService
from infrastructure.repositories.cliente_repository import ClienteRepository
from infrastructure.config.db.dbconfig import conexionDB
from typing import List

router = APIRouter()

# Inyectar el servicio usando la sesión de base de datos
def get_cliente_service(db: AsyncSession = Depends(conexionDB)) -> ClienteService:
    cliente_repo = ClienteRepository(db)
    return ClienteService(cliente_repo)

@router.post("/clientes/", response_model=ClienteRead)
async def crear_cliente(
    cliente_data: ClienteCreate, 
    cliente_service: ClienteService = Depends(get_cliente_service)
):
    try:
        return await cliente_service.crear_cliente(cliente_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/clientes/{cliente_id}", response_model=ClienteRead)
async def obtener_cliente_por_id(
    cliente_id: int, 
    cliente_service: ClienteService = Depends(get_cliente_service)
):
    try:
        return await cliente_service.obtener_cliente_por_id(cliente_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/clientes/", response_model=List[ClienteRead])
async def obtener_clientes(cliente_service: ClienteService = Depends(get_cliente_service)):
    return await cliente_service.obtener_clientes()

@router.put("/clientes/{cliente_id}", response_model=ClienteRead)
async def actualizar_cliente(
    cliente_id: int, 
    cliente_data: ClienteUpdate, 
    cliente_service: ClienteService = Depends(get_cliente_service)
):
    try:
        return await cliente_service.actualizar_cliente(cliente_id, cliente_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/clientes/{cliente_id}")
async def eliminar_cliente(
    cliente_id: int, 
    cliente_service: ClienteService = Depends(get_cliente_service)
):
    try:
        await cliente_service.eliminar_cliente(cliente_id)
        return {"message": "Cliente eliminado exitosamente"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
