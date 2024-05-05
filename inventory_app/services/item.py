from typing import Dict, Any, Union
from ..schemas.item import Item, PatchItem
from ..exceptions import ItemNotFound, ItemAlreadyExists


class ItemService:
    def __init__(self, items_contents: Dict[str, Dict[str, Any]]) -> None:
        self.items_contents = items_contents


    async def get_item_info(self, item_id: str) -> Item:
        if item_id not in self.items_contents:
            raise ItemNotFound(item_id)
        return Item(**self.items_contents[item_id])


    async def create_item(self, item: Item) -> Union[str, None]:
        if item.name:
            item_id = item.name.replace(' ', '').lower()
        if item_id in self.items_contents:
            raise ItemAlreadyExists(item_id)
        self.items_contents[item_id] = item.model_dump()
        return item_id


    async def update_item_db(self, item_id: str, item: Item) -> bool:
        item_exists = item_id in self.items_contents
        self.items_contents[item_id] = item.model_dump()
        return item_exists


    async def patch_item_db(self, item_id: str, item: PatchItem) -> bool:
        item_patched = False
        if item_id not in self.items_contents:
            raise ItemNotFound(item_id)
        for attribute in vars(item):
            value = getattr(item, attribute)
            if value and (value != self.items_contents[item_id].get(attribute)):
                self.items_contents[item_id][attribute] = value
                item_patched = True
        return item_patched


    async def delete_item_db(self, item_id: str) -> None:
        if item_id not in self.items_contents:
            raise ItemNotFound(item_id)
        del self.items_contents[item_id]