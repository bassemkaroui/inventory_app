from pydantic import BaseModel, Field
from typing import List, Optional

class Inventory(BaseModel):
    id: int = Field(ge=0, le=1_000_000)
    name: Optional[str] = None
    description: Optional[str] = None
    items_ids: List[str] = Field(
        description="Items' ids",
        min_length=1,
        max_length=50_000
    )