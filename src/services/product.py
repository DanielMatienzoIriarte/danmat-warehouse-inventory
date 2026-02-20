from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException

from src.database import IProductRepository
from src.database.models.product import Product

import uuid


class ProductService:
    def __init__(self, product_repository: IProductRepository):
        self.product_repository:IProductRepository = product_repository

    async def get_product(self, product_id:uuid.UUID) -> Product:
        product = await self.product_repository.get_product_by_id(product_id)
        if not product:
            raise ValueError("Product doesn't exist")
        
        return product

    async def save_product(self, product: Product):
        await self.product_repository.save(product)

        return product
'''
    async def get_by_id(self, db_session: AsyncSession, product_id: uuid.UUID) -> Product:
        product = await db_session.scalars(select(Product).where(Product.product_id == product_id)).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product Not Found")
        return product
'''