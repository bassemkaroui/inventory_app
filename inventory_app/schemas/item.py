from pydantic import BaseModel, Field
from typing import List, Optional


class Item(BaseModel):
    name: str
    price: float = Field(gt=0, lt=100_000)
    description: str = Field(max_length=250)

class PatchItem(BaseModel):
    name: Optional[str] = None
    price: float = Field(gt=0, lt=100_000, default=None)
    description: str = Field(max_length=250, default=None)


class VerboseItem(Item):
    full_description: str = Field(max_length=2048)


class CreateUpdateItemResponse(BaseModel):
    item_id: Optional[str] = None
    message: str


class MultipleItemsResponse(BaseModel):
    items: List[Item]
    total: int = Field(ge=0)
