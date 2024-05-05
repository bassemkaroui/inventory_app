import stat
import pytest
from aioresponses import aioresponses
from sample_requests.async_requests import sample_async_get_request, sample_async_post_request


@pytest.mark.asyncio
async def test_sample_async_get_request(existing_item_content):
    base_url = 'http://placeholder'
    endpoint_prefix = '/item/'
    item_id = 'item1'

    with aioresponses() as m:
        m.get(
            f'{base_url}{endpoint_prefix}{item_id}',
            status=200,
            payload=existing_item_content
        )
        status_code, json_response = await sample_async_get_request(base_url, endpoint_prefix, item_id)

    assert status_code == 200
    assert json_response == existing_item_content

@pytest.mark.asyncio
async def test_sample_async_post_request(new_item_content, new_item_id):
    base_url = 'http://placeholder'
    endpoint = '/item/'

    json_response = {
        'message': 'Item created successfully', 
        'item_id': new_item_id
    }

    with aioresponses() as m:
        m.post(
            f'{base_url}{endpoint}',
            status=201,
            payload=json_response
        )
        status_code, json_response = await sample_async_post_request(base_url, endpoint, new_item_content)

    assert status_code == 201
    assert json_response == json_response