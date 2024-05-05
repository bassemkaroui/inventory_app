from sqlalchemy import Column, String, Float, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from uuid import uuid4
from .base import Base

class Item(Base):
    __tablename__ = 'item'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    # updated_at
    name = Column(String, unique=True, nullable=False)
    price = Column(Float)
    description = Column(String(250))

    inventories = relationship('Inventory', secondary='inventory_item', back_populates='items')
