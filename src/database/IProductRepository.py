from abc import abstractmethod
from typing import Protocol, List
import uuid

from src.database.models.product import Product


class IProductRepository(Protocol):

    @abstractmethod
    async def get_by_id(self, id: uuid.UUID) -> Product:
        pass

    @abstractmethod
    async def get_all(self) -> List[Product]:
        pass

    @abstractmethod
    async def save(self, product: Product) -> uuid.UUID:
        pass