import asyncio
import aiohttp
from typing import Tuple
from pprint import pprint


async def sample_async_get_request(base_url: str, endpoint_prefix: str, item_id: str) -> Tuple[int, dict]:
    url = f'{base_url}{endpoint_prefix}{item_id}'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            json_response = await response.json()
            status_code = response.status
            return status_code, json_response




async def sample_async_post_request(base_url: str, endpoint: str, sample_data: dict) -> Tuple[int, dict]:
    url = f'{base_url}{endpoint}'
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=sample_data) as response:
            status_code = response.status
            json_response = await response.json()
            return status_code, json_response

if __name__ == '__main__':

    base_url = 'http://127.0.0.1:8000'
    endpoint_prefix = '/item/'
    item_id = 'item1'

    sample_data = {'name': 'Item 1000', 'price': 100.99, 'description': 'Description 10'}

    pprint(asyncio.run(sample_async_get_request(base_url, endpoint_prefix, item_id)))
    pprint(asyncio.run(sample_async_post_request(base_url, endpoint_prefix, sample_data)))
    pprint(asyncio.run(sample_async_post_request(base_url, endpoint_prefix, sample_data)))