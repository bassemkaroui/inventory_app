import pytest


@pytest.fixture(scope="class")
def testing_fixture():
    print("setup")
    yield 1
    print("teardown")


@pytest.fixture(scope="session")
def valid_item_id():
    return "item1"


@pytest.fixture(scope="session")
def invalid_item_id():
    return "abcdef"


@pytest.fixture
def items_contents():
    val = {
        "item1": {"name": "Item 1", "price": 10.99, "description": "Description 1"},
        "item2": {"name": "Item 2", "price": 20.99, "description": "Description 2"},
        "item3": {"name": "Item 3", "price": 30.99},
        "item4": {"name": "Item 4", "price": 40.99},
    }
    return val


@pytest.fixture
def existing_item_content(valid_item_id, items_contents):
    return items_contents[valid_item_id]


@pytest.fixture
def new_item_id():
    return "newitem"


@pytest.fixture
def new_item_content(items_contents, valid_item_id, new_item_id):
    item_content = items_contents[valid_item_id]
    item_content["name"] = new_item_id
    return item_content
