from fastapi import FastAPI
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Numeric
from decimal import Decimal

import uuid


class Product(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)  # Enables Pydantic to read from ORM attributes

    product_id: Mapped[uuid.UUID] = mapped_column(default_factory=uuid.uuid4, primary_key=True, index=True, nullable=False)
    sku: Mapped[str] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    image: Mapped[str] = mapped_column(default="default_product.jpg", nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(precision=10, scale=2), default=Decimal(0.00), nullable=False)
    quantity: Mapped[int] = mapped_column(nullable=False)