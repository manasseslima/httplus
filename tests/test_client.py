import pytest
from skate.client import Client


@pytest.mark.asyncio
async def test_basic_client_request():
    url = 'https://pokeapi.co/api/v2/berry?limit=20&offset=20'
    client = Client()
    res = await client.get(url)
    assert res
