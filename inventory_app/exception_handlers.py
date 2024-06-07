from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from . import ItemAlreadyExists, ItemNotFound
from .logger import create_logger

logger = create_logger(__name__)


def add_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(ItemNotFound)
    async def item_not_found_exception_handler(
        request: Request, exc: ItemNotFound
    ) -> JSONResponse:
        logger.error(f"Item with id {exc.item_id!r} not found")
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "Item not found", "item_id": exc.item_id},
        )

    @app.exception_handler(ItemAlreadyExists)
    async def item_exists_exception_handler(
        request: Request, exc: ItemAlreadyExists
    ) -> JSONResponse:
        logger.error(f"Item with id {exc.item_id!r} already exists")
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "message": (
                    f"An item with the id {exc.item_id!r} is already in the database"
                ),
                "item_id": None,
            },
        )
