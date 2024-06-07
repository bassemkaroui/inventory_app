from typing import Any, Callable, Dict

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from ..logger import create_logger
from ..schemas.item import CreateUpdateItemResponse, Item, PatchItem
from ..services.item import ItemService

logger = create_logger(__name__)


def create_item_router(
    rate_limiter: Callable, items_contents: Dict[str, Dict[str, Any]]
) -> APIRouter:

    item_router = APIRouter(
        prefix="/item", tags=["Item"], dependencies=[Depends(rate_limiter)]
    )
    item_service = ItemService(items_contents)

    @item_router.get("/{item_id}", response_model=Item)
    async def get_item_by_id(item_id: str) -> Item:
        item = await item_service.get_item_info(item_id)
        return item

    @item_router.post(
        "/",
        response_model=CreateUpdateItemResponse,
        status_code=status.HTTP_201_CREATED,
    )
    async def add_item(item: Item) -> CreateUpdateItemResponse:
        # Add the item to the dictionary items_contents
        # The item id will be the name of the item stripped of spaces
        # and lowercased
        item_id = await item_service.create_item(item)
        return CreateUpdateItemResponse(
            item_id=item_id, message="Item added successfully to the database"
        )

    @item_router.put("/{item_id}", response_model=CreateUpdateItemResponse)
    async def update_item(item_id: str, item: Item) -> JSONResponse:
        # Update the item in the dictionary items_contents or create it if it
        # doesn't exist
        item_exists = await item_service.update_item_db(item_id, item)
        response_content = CreateUpdateItemResponse(
            message=(
                "Item updated successfully"
                if item_exists
                else "Item created successfully"
            ),
            item_id=item_id,
        )
        return JSONResponse(
            status_code=status.HTTP_200_OK if item_exists else status.HTTP_201_CREATED,
            content=response_content.model_dump(),
        )

    @item_router.patch("/{item_id}", response_model=CreateUpdateItemResponse)
    async def patch_item(item_id: str, item: PatchItem) -> CreateUpdateItemResponse:
        item_patched = await item_service.patch_item_db(item_id, item)
        return CreateUpdateItemResponse(
            item_id=item_id,
            message=(
                "The item was patched successfully"
                if item_patched
                else "The item was not patched"
            ),
        )

    @item_router.delete("/{item_id}")
    async def delete_item(item_id: str) -> JSONResponse:
        # Delete the item from the dictionary items_contents.
        await item_service.delete_item_db(item_id)
        return JSONResponse(content={"message": "Item deleted successfully"})

    return item_router
