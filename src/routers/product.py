import uuid
from fastapi import APIRouter, Depends

from src.database.models.product import Product
from src.dependencies.product_dependencies import db_session_dependency
from src.services.product import ProductService


router = APIRouter(
    prefix="/api/product",
    tags=["products"],
    responses={404: {"description": "Not Found"}},
)

@router.get(
    "/{product_id}",
    response_model=Product,
    summary="Get a single product item"
)
async def get_product(
    product_id: uuid.UUID,
):
    product = await ProductService.get_product(product_id)
    return product


@router.get(
    "/aux/{product_id}",
    response_model=Product,
    summary="Get a single product item"
)
async def get(
    product_id: uuid.UUID,
    db_session: db_session_dependency,
):
    product = await ProductService.get_by_id(db_session, product_id)
    return product
"""
@router.post(
    "/",
    response_model=Product,
    summary="Save a product item"
)
async def save(
    request
):
    product_id = await ProductService.save()"""