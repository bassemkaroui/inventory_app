from datetime import datetime
from sqlalchemy import TIMESTAMP, Column, String
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
from .base import Base


class Inventory(Base):
    __tablename__ = 'inventory'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    created_at = Column(TIMESTAMP(), default=datetime.utcnow)
    name = Column(String(250), nullable=False)
    description = Column(String(250))

    items = relationship('Item', secondary='inventory_item', back_populates='inventories')
    