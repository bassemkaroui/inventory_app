from typing import List, Tuple, Dict, Any
from ..schemas.item import Item
from ..schemas.inventory import Inventory


class InventoryService:
    def __init__(
        self,
        items_contents: Dict[str, Dict[str, Any]],
        inventories_contents: Dict[int, Dict[str, Any]]
    ) -> None:
        self.items_contents = items_contents
        self.inventories_contents = inventories_contents

    async def get_inventory(self, inventory_id: int) -> Inventory:
        inventory = Inventory(
            id=inventory_id,
            items_ids=self.inventories_contents[inventory_id]['items_ids']
        )
        return inventory

    async def get_items_with_pagination(self, inventory_id: int, start: int, limit: int) -> Tuple[List[Item], int]:
        inventory = await self.get_inventory(inventory_id)
        filtered_items_ids = inventory.items_ids[start:start+limit]
        items = [Item(**self.items_contents[item_id])
                 for item_id in filtered_items_ids]
        return items, len(inventory.items_ids)

    async def add_item_to_inventory_db(self, inventory_id: int, item: Item) -> Tuple[str, str]:
        if item.name:
            item_id = item.name.replace(' ', '').lower()
        item_dict = item.model_dump()
        inventory = await self.get_inventory(inventory_id)
        if item_id not in self.items_contents:
            self.items_contents[item_id] = item_dict
            # Add the item to the inventory
            inventory.items_ids.append(item_id)
            return "Item added successfully to the database and inventory", item_id
        else:
            if (item_id, item_dict) in self.items_contents.items():
                if item_id not in inventory.items_ids:
                    # Add the item to the inventory
                    inventory.items_ids.append(item_id)
                    return "Item added successfully to the inventory", item_id
                return "The item is already in the inventory", item_id
            else:
                return "An item with the same id is already in the database", item_id
