import pytest

from inventory_app.services.item import ItemService


@pytest.fixture
def _inventories_contents():
    val = {
        0: {"id": 0, "items_ids": ["item1", "item2", "item3", "item4"]},
        1: {"id": 1, "items_ids": ["item2", "item3", "item4"]},
        2: {"id": 2, "items_ids": ["item3", "item4"]},
        3: {"id": 3, "items_ids": ["item1", "item2", "item3"]},
    }
    return val


@pytest.fixture
def item_service(items_contents):
    val = ItemService(items_contents)
    return val
