from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from .base import Base


class InventoryItem(Base):
    __tablename__ = 'inventory_item'
    
    inventory_id = Column(UUID(as_uuid=True), ForeignKey('inventory.id'), primary_key=True)
    item_id = Column(UUID(as_uuid=True), ForeignKey('item.id'), primary_key=True, index=True)

    quantity = Column(Integer)