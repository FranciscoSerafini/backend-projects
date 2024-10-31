from abc import ABC, abstractmethod
from typing import List, Optional
from application.dtos.cliente_dtos import ClienteCreate, ClienteUpdate, ClienteRead

class ClienteRepoInterface(ABC):
    
    @abstractmethod
    async def crear_cliente(self, cliente: ClienteCreate) -> ClienteRead:
        """Crear un nuevo cliente."""
        pass
    
    @abstractmethod
    async def obtener_cliente_por_id(self, cliente_id: int) -> Optional[ClienteRead]:
        """Obtener un cliente por su ID."""
        pass

    @abstractmethod
    async def obtener_clientes(self) -> List[ClienteRead]:
        """Obtener todos los clientes."""
        pass
    
    @abstractmethod
    async def actualizar_cliente(self, cliente_id: int, cliente: ClienteUpdate) -> Optional[ClienteRead]:
        """Actualizar un cliente existente."""
        pass
    
    @abstractmethod
    async def eliminar_cliente(self, cliente_id: int) -> bool:
        """Eliminar un cliente por su ID."""
        pass
