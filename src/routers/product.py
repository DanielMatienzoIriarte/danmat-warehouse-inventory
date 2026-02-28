import string
import uuid
from typing import AsyncGenerator, List
from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from watchfiles import awatch

from src.database.models.product import Product
from src.services.product import ProductService
from src.schemas.product import Product as ProductSchema

router = APIRouter(
    prefix="/api/product",
    tags=["products"]
)


async def get_session(request: Request) -> AsyncGenerator[AsyncSession, None]:
    session_factory = request.app.state.postgres_pool
    async with session_factory() as session:
        yield session

def get_product_service(session: AsyncSession = Depends(get_session)):
    return ProductService(session)

@router.get(
    "/{product_id}",
    response_model=Product,
    summary="Get a single product item"
)
async def get_product(
    product_id: uuid.UUID,
    service: ProductService = Depends(get_product_service),
):
    product = await service.get_product(product_id)
    return product

@router.post(
    "/",
    response_model=Product,
    summary="Create a product item"
)
async def create_product(
    product: ProductSchema,
    product_service: ProductService = Depends(get_product_service),
):
    product = await product_service.create_product(product)
    return product

@router.get(
    "/",
    response_model=List[Product],
    summary="Get all products"
)
async def get_all_products(
    service: ProductService = Depends(get_product_service),
):
    products:List[Product] = await service.get_all_products()
    return products

@router.patch(
    "/{product_id}/{process}/{quantity}",
    response_model=Product,
    summary="Update a product's quantity"
)
async def update_quantity(
    product_id : uuid.UUID,
    process: str,
    quantity: int,
    product_service: ProductService = Depends(get_product_service),
):
    try:
        return await product_service.update_quantity(product_id, process, quantity)
    except ValueError as err:
        raise HTTPException(status_code=400, detail=str(err))

@router.put(
    "/{product_id}",
    response_model=Product,
    summary="Update a product's data"
)
async def update_product(
        product_id: uuid.UUID,
        payload:ProductSchema,
        product_service: ProductService = Depends(get_product_service)
):
    try:
        return await product_service.update(product_id, payload)
    except ValueError as err:
        raise HTTPException(status_code=400, detail=str(err))