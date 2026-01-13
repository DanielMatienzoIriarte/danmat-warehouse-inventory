import uuid
from dataclasses import dataclass
from decimal import Decimal
from sqlalchemy import Numeric
from sqlalchemy.orm import Mapped, mapped_column
from src.database.models.base import Base


class Product(Base):
    __tablename__ = "products"

    sku: Mapped[str] = mapped_column()
    name: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    product_id: Mapped[uuid.UUID] = mapped_column(default_factory=uuid.uuid4, primary_key=True, index=True, nullable=False)
    image: Mapped[str] = mapped_column(default="default_product.jpg", nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(precision=10, scale=2), default=Decimal(0.00), nullable=False)
    quantity: Mapped[int] = mapped_column(default=1, nullable=False)