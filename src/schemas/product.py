import uuid

from decimal import Decimal
from pydantic import BaseModel, ConfigDict


class Product(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    sku: str
    name: str
    description: str
    image: str 
    price: Decimal
    quantity: int