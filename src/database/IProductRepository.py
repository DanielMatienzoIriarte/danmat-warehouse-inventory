from abc import abstractmethod
from typing import Protocol, List
from dataclasses import dataclass
import uuid

from src.database.models.product import Product


class IProductRepository(Protocol):
    async def get_by_id(self, id: uuid.UUID) -> Product:
        pass

    async def get_all(self) -> List[Product]:
        pass

    async def save(self, product: Product) -> uuid.UUID:
        pass