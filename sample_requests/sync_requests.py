import json
import os

# from pprint import pprint
from urllib.parse import urljoin

import requests
from requests import Response

# base_url = 'http://127.0.0.1:8000'

# response = requests.get(base_url+'/item/item1')

# print(response.status_code)
# print(response.headers)
# pprint(response.json())


# sample_data = {'name': 'Item 1000', 'price': 100.99, 'description': 'Description 10'}
# response = requests.post(base_url+'/item/', json=sample_data)
# # response = requests.post(base_url+'/item/', data=json.dumps(sample_data))
# print(response.status_code)
# pprint(response.json())


def get_item(base_url: str, endpoint: str, item_id: str) -> dict | None:
    url = urljoin(base_url, os.path.join(endpoint, item_id))
    response = requests.get(url)
    if response.ok:
        return response.json()
    return None


def create_item(base_url: str, endpoint: str, item_data: dict) -> Response:
    url = urljoin(base_url, endpoint)
    response = requests.post(url, json=item_data)
    return response


##############################################################################


def len_joke() -> int:
    joke = get_joke()
    return len(joke)


def get_joke() -> str:
    url = "https://api.chucknorris.io/jokes/random"
    response = requests.get(url)
    if response.ok:
        return response.json()["value"]
    return "No joke available"


def get_cat_fact() -> tuple[int, dict] | str:
    url = "https://meowfacts.herokuapp.com/"
    response = requests.get(url)

    # if response.ok:
    if response.status_code in (200, 201):
        return response.status_code, response.json()
    else:
        return json.dumps({"ERROR": "Cat Fact Not Available"})


if __name__ == "__main__":
    print(get_joke())
