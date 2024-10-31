from application.interfaces.cliente_repo_interface import ClienteRepoInterface
from application.dtos.cliente_dtos import ClienteCreate, ClienteUpdate, ClienteRead
from typing import List, Optional

class ClienteService:
    def __init__(self, cliente_repo: ClienteRepoInterface):
        self.cliente_repo = cliente_repo

    async def crear_cliente(self, cliente_data: ClienteCreate) -> ClienteRead:
        try:
            return await self.cliente_repo.crear_cliente(cliente_data)
        except ValueError as e:
            # Manejo de errores específicos de negocio, por ejemplo, DNI duplicado
            raise ValueError(f"Error al crear el cliente: {e}")

    async def obtener_cliente_por_id(self, cliente_id: int) -> Optional[ClienteRead]:
        cliente = await self.cliente_repo.obtener_cliente_por_id(cliente_id)
        if cliente is None:
            raise ValueError(f"Cliente con ID {cliente_id} no encontrado.")
        return cliente

    async def obtener_clientes(self) -> List[ClienteRead]:
        return await self.cliente_repo.obtener_clientes()

    async def actualizar_cliente(self, cliente_id: int, cliente_data: ClienteUpdate) -> Optional[ClienteRead]:
        try:
            cliente_actualizado = await self.cliente_repo.actualizar_cliente(cliente_id, cliente_data)
            if cliente_actualizado is None:
                raise ValueError(f"Cliente con ID {cliente_id} no encontrado para actualizar.")
            return cliente_actualizado
        except ValueError as e:
            raise ValueError(f"Error al actualizar el cliente: {e}")

    async def eliminar_cliente(self, cliente_id: int) -> bool:
        eliminado = await self.cliente_repo.eliminar_cliente(cliente_id)
        if not eliminado:
            raise ValueError(f"Cliente con ID {cliente_id} no encontrado para eliminar.")
        return eliminado
