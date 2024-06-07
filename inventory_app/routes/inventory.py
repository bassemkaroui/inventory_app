from typing import Any, Callable, Dict

from fastapi import APIRouter, Depends, status
from fastapi.responses import RedirectResponse

from ..schemas.item import CreateUpdateItemResponse, Item, MultipleItemsResponse
from ..services.inventory import InventoryService


def create_inventory_router(
    rate_limiter: Callable,
    items_contents: Dict[str, Dict[str, Any]],
    inventories_contents: Dict[int, Dict[str, Any]],
) -> APIRouter:

    inventory_router = APIRouter(
        prefix="/inventory", tags=["Inventory"], dependencies=[Depends(rate_limiter)]
    )

    inventory_service = InventoryService(items_contents, inventories_contents)

    # This route needs to be here otherwise the request '/inventory/main' will go
    # through '/inventory/{inventory_id}' which will generate an error
    @inventory_router.get(
        "/main",
        response_model=MultipleItemsResponse,
        status_code=status.HTTP_301_MOVED_PERMANENTLY,
    )
    async def get_main_inventory() -> RedirectResponse:
        # Fetch the inventory from the database
        # main_inventory = create_inventory(0)
        limit = len(inventories_contents[0]["items_ids"])
        return RedirectResponse(
            f"/api/v1/inventory/0?start=0&limit={limit}",
            status_code=status.HTTP_301_MOVED_PERMANENTLY,
        )

    # Query parameters are used to filter the items (pagination).
    # Request URL will look like this: /inventory/1?start=0&limit=3
    @inventory_router.get("/{inventory_id}", response_model=MultipleItemsResponse)
    async def get_items_from_inventory(
        inventory_id: int, start: int = 0, limit: int = 3
    ) -> MultipleItemsResponse:
        """
        Get items from the inventory

        Args:
        inventory_id (int): The id of the inventory
        start (int): The start index of the items to return
        limit (int): The number of items to return

        Returns:
        MultipleItemsResponse: The items from the inventory
        """

        # Fetch the inventory from the database
        # Then return the items from the inventory
        items, total = await inventory_service.get_items_with_pagination(
            inventory_id, start, limit
        )
        return MultipleItemsResponse(items=items, total=total)

    @inventory_router.post("/{inventory_id}", response_model=CreateUpdateItemResponse)
    async def add_item_to_inventory(
        inventory_id: int, item: Item
    ) -> CreateUpdateItemResponse:
        # Add the item to the dictionary items_contents then add it to the inventory
        # The item id will be the name of the item stripped of spaces and lowercased
        message, item_id = await inventory_service.add_item_to_inventory_db(
            inventory_id, item
        )
        return CreateUpdateItemResponse(message=message, item_id=item_id)

    return inventory_router
