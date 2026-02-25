import uuid
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.database.models.product import Product
from src.schemas.product import Product as ProductSchema


class ProductRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    """
    """
    async def get_by_id(self, product_id:uuid.UUID) -> Product:
        query = select(Product).where(Product.product_id == product_id)
        result = await self.db_session.execute(query)
        product:Product = result.scalars().first()

        return product

    """
    """
    async def get_all(self) -> List[Product]:
        query = select(Product).order_by(Product.sku)
        result = await self.db_session.execute(query)
        products:List[Product] = list(result.scalars().all())

        return products

    """

    """    
    async def create(self, product_data: ProductSchema) -> Product:
        product = Product(**product_data.model_dump())
        self.db_session.add(product)
        await self.db_session.commit()
        await self.db_session.refresh(product)
        """query = "INSERT INTO users (email, password) VALUES (:email, :password) RETURNING id"
        values = {
            "name": product.name,
            "description": product.description,
            "SKU": product.sku,
            "image": product.image,
            "price": product.price,
            "quantity": product.quantity
        }
        new_product_id = await self.db_session.execute(query, values)"""

        return product