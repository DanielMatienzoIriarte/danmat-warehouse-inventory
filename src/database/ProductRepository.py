import uuid
from itertools import product
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

        return product

    """
    """
    async def update_quantity(self, product_id:uuid.UUID, process: str, quantity:int) -> Product:
        result = await self.db_session.execute(
            select(Product).where(Product.product_id == product_id)
        )
        product = result.scalars().one_or_none()

        if not product:
            raise ValueError(f"Product with id {product_id} not found")

        if process == "purchase":
            product.quantity += quantity
        elif process == "sale":
            if quantity > product.quantity:
                raise ValueError(f"Quantity must not be greater than {product.quantity}")
            else:
                product.quantity -= quantity

        await self.db_session.commit()
        await self.db_session.refresh(product)

        return product

    async def update(self,
        product_id:uuid.UUID,
        product: ProductSchema
    ):
        result = await self.db_session.execute(
            select(Product).where(Product.product_id == product_id)
        )
        current_product = result.scalars().one_or_none()

        if not current_product:
            raise ValueError(f"Product with id {product_id} not found")

        if product.name is not None:
            current_product.name = product.name
        if product.description is not None:
            current_product.description = product.description
        if product.image is not None:
            current_product.image = product.image
        if product.price is not None:
            if product.price < 0.00:
                raise ValueError(f"Price must not be less than zero")
            current_product.price = product.price
        if product.quantity is not None:
            if product.quantity < 0:
                raise ValueError(f"Quantity must not be less than zero")
            current_product.quantity = product.quantity

        await self.db_session.commit()
        await self.db_session.refresh(current_product)

        return current_product