from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from domain.entities.cliente_modelo import Cliente
from application.dtos.cliente_dtos import ClienteCreate, ClienteUpdate, ClienteRead
from application.interfaces.cliente_repo_interface import ClienteRepoInterface
from typing import List, Optional

class ClienteRepository(ClienteRepoInterface):
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def crear_cliente(self, cliente: ClienteCreate) -> ClienteRead:
        nuevo_cliente = Cliente(
            cli_dni=cliente.dni,
            cli_nombre=cliente.nombre,
            cli_apellido=cliente.apellido,
            cli_direccion=cliente.direccion,
            cli_correo=cliente.correo,
            cli_celular=cliente.celular,
            cli_id_tipo=cliente.id_tipo,
    )
        self.db_session.add(nuevo_cliente)
        try:
            await self.db_session.commit()
            await self.db_session.refresh(nuevo_cliente)
            return ClienteRead.model_validate({
                'dni': nuevo_cliente.cli_dni,
                'nombre': nuevo_cliente.cli_nombre,
                'apellido': nuevo_cliente.cli_apellido,
                'direccion': nuevo_cliente.cli_direccion,
                'correo': nuevo_cliente.cli_correo,
                'celular': nuevo_cliente.cli_celular,
                'id_tipo': nuevo_cliente.cli_id_tipo,
            })
        except IntegrityError:
         await self.db_session.rollback()
        raise ValueError("El DNI ya existe en la base de datos.")

    async def obtener_cliente_por_id(self, cliente_id: int) -> Optional[ClienteRead]:
        query = select(Cliente).where(Cliente.cli_id == cliente_id)
        result = await self.db_session.execute(query)
        cliente = result.scalars().first()
        if cliente:
             return ClienteRead.model_validate({
            'dni': cliente.cli_dni,
            'nombre': cliente.cli_nombre,
            'apellido': cliente.cli_apellido,
            'direccion': cliente.cli_direccion,
            'correo': cliente.cli_correo,
            'celular': cliente.cli_celular,
            'id_tipo': cliente.cli_id_tipo,
        })
        return None

    async def obtener_clientes(self) -> List[ClienteRead]:
        query = select(Cliente)
        result = await self.db_session.execute(query)
        clientes = result.scalars().all()
    
        # Usar un diccionario con comprensión de lista
        return [ClienteRead.model_validate({
            'dni': cliente.cli_dni,
            'nombre': cliente.cli_nombre,
            'apellido': cliente.cli_apellido,
            'direccion': cliente.cli_direccion,
            'correo': cliente.cli_correo,
            'celular': cliente.cli_celular,
            'id_tipo': cliente.cli_id_tipo,
        }) for cliente in clientes]

    async def actualizar_cliente(self, cliente_id: int, cliente_data: ClienteUpdate) -> Optional[ClienteRead]:
        query = select(Cliente).where(Cliente.cli_id == cliente_id)
        result = await self.db_session.execute(query)
        cliente = result.scalars().first()
        
        if cliente:
            for key, value in cliente_data.dict(exclude_unset=True).items():
                setattr(cliente, f"cli_{key}", value)
            
            try:
                await self.db_session.commit()
                await self.db_session.refresh(cliente)
                return ClienteRead.model_validate({
                    'dni': cliente.cli_dni,
                    'nombre': cliente.cli_nombre,
                    'apellido': cliente.cli_apellido,
                    'direccion': cliente.cli_direccion,
                    'correo': cliente.cli_correo,
                    'celular': cliente.cli_celular,
                    'id_tipo': cliente.cli_id_tipo,
                })
            except IntegrityError:
                await self.db_session.rollback()
                raise ValueError("Error al actualizar el cliente.")
        return None

    async def eliminar_cliente(self, cliente_id: int) -> bool:
        query = select(Cliente).where(Cliente.cli_id == cliente_id)
        result = await self.db_session.execute(query)
        cliente = result.scalars().first()
        if cliente:
            await self.db_session.delete(cliente)
            await self.db_session.commit()
            return True
        return False
