from fastapi import status


def test_get_item_by_id_successfully(testing_app, valid_item_id, existing_item_content):
    response = testing_app.get(f"/item/{valid_item_id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == existing_item_content


def test_get_item_by_id_fails(testing_app, invalid_item_id):
    response = testing_app.get(f"/item/{invalid_item_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"message": "Item not found", "item_id": invalid_item_id}


def test_create_item_successfully(testing_app, new_item_content, new_item_id):
    response = testing_app.post("/item/", json=new_item_content)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {
        "item_id": new_item_id,
        "message": "Item added successfully to the database",
    }


def test_create_item_already_exists(testing_app, valid_item_id, existing_item_content):
    item = existing_item_content.copy()
    item["price"] = 50.99
    response = testing_app.post("/item/", json=item)
    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json() == {
        "message": f"An item with the id {valid_item_id!r} is already in the database",
        "item_id": None,
    }


def test_update_item_successfully(testing_app, valid_item_id, existing_item_content):
    item = existing_item_content.copy()
    item["price"] = 50.99
    response = testing_app.put(f"/item/{valid_item_id}", json=item)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "message": "Item updated successfully",
        "item_id": valid_item_id,
    }
    response = testing_app.get(f"/item/{valid_item_id}")
    assert response.json() == item


def test_creating_item_from_update_endpoint(testing_app, new_item_content, new_item_id):
    response = testing_app.put(f"/item/{new_item_id}", json=new_item_content)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {
        "message": "Item created successfully",
        "item_id": new_item_id,
    }
    response = testing_app.get(f"/item/{new_item_id}")
    assert response.json() == new_item_content


def test_patch_item_successfully(testing_app, existing_item_content, valid_item_id):
    item = existing_item_content.copy()
    item["price"] = 50.99
    copy_item = item.copy()
    del item["name"], item["description"]
    response = testing_app.patch(f"/item/{valid_item_id}", json=item)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "message": "The item was patched successfully",
        "item_id": valid_item_id,
    }
    response = testing_app.get(f"/item/{valid_item_id}")
    assert response.json() == copy_item


def test_patch_item_fails(testing_app, existing_item_content, invalid_item_id):
    response = testing_app.patch(f"/item/{invalid_item_id}", json=existing_item_content)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"message": "Item not found", "item_id": invalid_item_id}


def test_patch_item_with_no_modification_1(
    testing_app, existing_item_content, valid_item_id
):
    item = {}
    response = testing_app.patch(f"/item/{valid_item_id}", json=item)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "message": "The item was not patched",
        "item_id": valid_item_id,
    }
    response = testing_app.get(f"/item/{valid_item_id}")
    assert response.json() == existing_item_content


def test_patch_item_with_no_modification_2(
    testing_app, existing_item_content, valid_item_id
):
    response = testing_app.patch(f"/item/{valid_item_id}", json=existing_item_content)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "message": "The item was not patched",
        "item_id": valid_item_id,
    }
    response = testing_app.get(f"/item/{valid_item_id}")
    assert response.json() == existing_item_content


def test_delete_item_successfully(testing_app, valid_item_id):
    response = testing_app.delete(f"/item/{valid_item_id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "Item deleted successfully"}


def test_double_delete_item_error(testing_app, valid_item_id):
    response = testing_app.delete(f"/item/{valid_item_id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "Item deleted successfully"}
    response = testing_app.delete(f"/item/{valid_item_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"message": "Item not found", "item_id": valid_item_id}


def test_delete_item_not_found(testing_app, invalid_item_id):
    response = testing_app.delete(f"/item/{invalid_item_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"message": "Item not found", "item_id": invalid_item_id}
