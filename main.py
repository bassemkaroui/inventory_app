from fastapi import FastAPI, Request
# from fastapi.responses import JSONResponse, PlainTextResponse
from typing import Dict, Any
from models import recreate_tables
from inventory_app import (
    create_item_router, 
    create_inventory_router, 
    create_divers_router,
    add_exception_handlers,
    create_rate_limiter,
    StrOrCallable
)

RATE_LIMIT_VALUE = "5/30seconds"

# application factory pattern
def create_app(rate_limit_value: StrOrCallable = RATE_LIMIT_VALUE) -> FastAPI:
    app = FastAPI(root_path="/api/v1")
    rate_limiter = create_rate_limiter(app, rate_limit_value)  

    items_contents, inventories_contents = create_items_inventories()

    divers_router = create_divers_router(rate_limiter)
    inventory_router = create_inventory_router(rate_limiter, items_contents, inventories_contents)
    item_router = create_item_router(rate_limiter, items_contents)

    app.include_router(divers_router)
    app.include_router(inventory_router)
    app.include_router(item_router)
    add_exception_handlers(app)
    
    return app

def create_items_inventories():
    items_contents: Dict[str, Dict[str, Any]] = {
        'item1' : {
            'name': 'Item 1',
            'price': 10.99,
            'description': 'Description 1'
        }, 
        'item2' : {
            'name': 'Item 2',
            'price': 20.99,
            'description': 'Description 2'
        },
        'item3' : {
            'name': 'Item 3',
            'price': 30.99,
            'description': 'Description 3'
        },
        'item4' : {
            'name': 'Item 4',
            'price': 40.99,
            'description': 'Description 4'
        }
    }

    inventories_contents: Dict[int, Dict[str, Any]] = {
        0: {
            'id': 0,
            'items_ids': ['item1', 'item2', 'item3', 'item4']
        },
        1: {
            'id': 1,
            'items_ids': ['item2', 'item3', 'item4']
        },
        2: {
            'id': 2,
            'items_ids': ['item3', 'item4']
        },
        3: {
            'id': 3,
            'items_ids': ['item1', 'item2', 'item3']
        }
    }
    return items_contents, inventories_contents

recreate_tables()

app = create_app()