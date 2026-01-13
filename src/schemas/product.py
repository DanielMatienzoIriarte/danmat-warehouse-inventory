from decimal import Decimal
import uuid
from pydantic import BaseModel, ConfigDict

class Product(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    product_id: uuid.UUID
    sku: str
    name: str
    description: str
    image: str 
    price: Decimal
    quantity: int