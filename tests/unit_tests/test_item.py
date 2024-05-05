import pytest
from inventory_app.schemas.item import Item, PatchItem
from inventory_app.exceptions import ItemNotFound, ItemAlreadyExists


@pytest.mark.asyncio
async def test_get_item_info_successfully(valid_item_id, item_service):
    item = await item_service.get_item_info(valid_item_id)
    assert item.name == 'Item 1'
    assert item.price == 10.99
    assert item.description == 'Description 1'

@pytest.mark.asyncio
async def test_get_item_info_fails(invalid_item_id, item_service):
    with pytest.raises(ItemNotFound):
        await item_service.get_item_info(invalid_item_id)

@pytest.mark.asyncio
async def test_create_item_successfully(item_service, new_item_content, new_item_id):
    item = Item(**new_item_content)
    item_id = await item_service.create_item(item)
    assert item_id == new_item_id
    assert item_service.items_contents[item_id] == new_item_content


@pytest.mark.asyncio
async def test_create_item_fails(item_service, existing_item_content):
    item_dict = existing_item_content.copy()
    item_dict['price'] = 50.89
    item = Item(**item_dict)
    with pytest.raises(ItemAlreadyExists):
        await item_service.create_item(item)

@pytest.mark.asyncio
async def test_update_item_db(valid_item_id, item_service, existing_item_content):
    item_dict = existing_item_content.copy()
    item_dict['price'] = 100.99
    item_exits = await item_service.update_item_db(valid_item_id, Item(**item_dict))
    assert item_exits
    assert item_service.items_contents[valid_item_id] == item_dict

@pytest.mark.asyncio
async def test_update_item_db_create_item(item_service, new_item_content, new_item_id):
    item = Item(**new_item_content)
    item_exits = await item_service.update_item_db(new_item_id, item)
    assert item_exits is False
    assert item_service.items_contents[new_item_id] == new_item_content

@pytest.mark.asyncio
async def test_patch_item_db_successfully(valid_item_id, item_service):
    item_dict = item_service.items_contents[valid_item_id].copy()
    item_dict['price'] = 100.99
    item_patched = await item_service.patch_item_db(valid_item_id, PatchItem(**item_dict))
    assert item_patched
    assert item_service.items_contents[valid_item_id] == item_dict

@pytest.mark.asyncio
async def test_patch_item_db_fails(invalid_item_id, item_service):
    item_dict = {'price': 100.99}
    with pytest.raises(ItemNotFound):
        await item_service.patch_item_db(invalid_item_id, PatchItem(**item_dict))

@pytest.mark.asyncio
async def test_delete_item_db_successfully(valid_item_id, item_service):
    await item_service.delete_item_db(valid_item_id)
    assert valid_item_id not in item_service.items_contents

@pytest.mark.asyncio
async def test_delete_item_db_fails(invalid_item_id, item_service):
    with pytest.raises(ItemNotFound):
        await item_service.delete_item_db(invalid_item_id)