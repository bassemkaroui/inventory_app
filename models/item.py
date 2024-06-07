from datetime import datetime
from uuid import uuid4

from sqlalchemy import TIMESTAMP, Column, Float, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .base import Base


class Item(Base):
    __tablename__ = "item"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    created_at = Column(TIMESTAMP(), default=datetime.utcnow)
    # updated_at
    name = Column(String(250), unique=True, nullable=False)
    price = Column(Float(), nullable=False)
    description = Column(String(250))

    inventories = relationship(
        "Inventory", secondary="inventory_item", back_populates="items"
    )
