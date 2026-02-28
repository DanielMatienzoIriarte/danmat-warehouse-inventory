import uuid
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.ProductRepository import ProductRepository
from src.database.models.product import Product
from src.schemas.product import Product as ProductSchema


class ProductService:
    def __init__(self, session: AsyncSession):
        self.product_repository:ProductRepository = ProductRepository(session)

    async def get_product(self, product_id:uuid.UUID) -> Product:
        product = await self.product_repository.get_by_id(product_id)
        if not product:
            raise ValueError("Product doesn't exist")
        
        return product

    async def create_product(self, product_schema: ProductSchema):
        product = await self.product_repository.create(product_schema)

        return product

    async def get_all_products(self) -> List[Product]:
        products = await self.product_repository.get_all()
        if not products:
            raise ValueError("Products doesn't exist")

        return products

    async def update_quantity(self, product_id:uuid.UUID, process: str, quantity:int):
        product = await self.product_repository.update_quantity(product_id, process, quantity)
        if not product:
            raise ValueError("Products doesn't exist")

        return product

    async def update(self, product_id:uuid.UUID, product_schema: ProductSchema):
        product = await self.product_repository.update(product_id, product_schema)

        return product
'''
    async def get_by_id(self, db_session: AsyncSession, product_id: uuid.UUID) -> Product:
        product = await db_session.scalars(select(Product).where(Product.product_id == product_id)).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product Not Found")
        return product
'''