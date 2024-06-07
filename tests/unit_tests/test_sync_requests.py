import json

import responses

from sample_requests.sync_requests import (
    create_item,
    get_cat_fact,
    get_item,
    get_joke,
    len_joke,
)


@responses.activate
def test_get_item_sucessfully(existing_item_content, valid_item_id):
    base_url = "http://placeholder"
    endpoint = "/item/"

    responses.add(
        responses.GET,
        f"{base_url}{endpoint}{valid_item_id}",
        json=existing_item_content,
        status=200,  # 'status' not 'status_code'
        headers={},
    )
    item = get_item(base_url, endpoint, valid_item_id)

    assert item is not None
    assert item == existing_item_content


@responses.activate
def test_get_item_fails(existing_item_content, invalid_item_id):
    base_url = "http://placeholder"
    endpoint = "/item/"

    responses.add(responses.GET, f"{base_url}{endpoint}{invalid_item_id}", status=404)

    item = get_item(base_url, endpoint, invalid_item_id)

    assert item is None


@responses.activate
def test_create_item_successfully(new_item_content, new_item_id):
    base_url = "http://placeholder"
    endpoint = "/item/"

    responses.add(
        responses.POST,
        f"{base_url}{endpoint}",
        json={"message": "Item created successfully", "item_id": new_item_id},
        status=201,
    )
    response = create_item(base_url, endpoint, new_item_content)

    assert response.status_code == 201
    assert response.json() == {
        "message": "Item created successfully",
        "item_id": new_item_id,
    }

    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == f"{base_url}{endpoint}"
    assert responses.calls[0].request.body.decode() == json.dumps(new_item_content)


@responses.activate
def test_get_joke_successfully():
    joke = "Chuck Norris can divide by zero"
    responses.add(
        responses.GET,
        "https://api.chucknorris.io/jokes/random",
        json={"value": joke},
        status=200,
    )
    response_joke = get_joke()
    assert response_joke == joke


@responses.activate
def test_get_joke_fails():
    joke = "No joke available"
    responses.add(responses.GET, "https://api.chucknorris.io/jokes/random", status=404)
    response_joke = get_joke()
    assert response_joke == joke


@responses.activate
def test_len_joke_method_1():
    joke = "Chuck Norris can divide by zero"
    responses.add(
        responses.GET,
        "https://api.chucknorris.io/jokes/random",
        json={"value": joke},
        status=200,
    )
    joke_length = len_joke()
    assert joke_length == len(joke)


def test_len_joke_method_2(monkeypatch):
    def mock_get_joke() -> str:
        return "Chuck Norris can divide by zero"

    monkeypatch.setattr("sample_requests.sync_requests.get_joke", mock_get_joke)

    joke_length = len_joke()
    assert joke_length == len("Chuck Norris can divide by zero")


def test_get_cat_fact_success_1(monkeypatch):

    class MockResponse:
        def __init__(self, status_code, json_data):
            self.status_code = status_code
            self.json_data = json_data

        def json(self):
            return self.json_data

        @property
        def ok(self):
            return self.status_code in (200, 201)

        def __call__(self, *args, **kwargs):
            return self

    monkeypatch.setattr("requests.get", MockResponse(200, {"data": "Cat Fact"}))

    status_code, cat_fact = get_cat_fact()
    assert status_code == 200
    assert cat_fact == {"data": "Cat Fact"}


def test_get_cat_fact_success_2(monkeypatch):

    class MockResponse:
        def __init__(self, status_code, json_data):
            self.status_code = status_code
            self.json_data = json_data

        def json(self):
            return self.json_data

        @property
        def ok(self):
            return self.status_code in (200, 201)

    def mock_get(*args, **kwargs) -> MockResponse:
        return MockResponse(200, {"data": "Cat Fact"})

    monkeypatch.setattr("requests.get", mock_get)

    status_code, cat_fact = get_cat_fact()
    assert status_code == 200
    assert cat_fact == {"data": "Cat Fact"}
