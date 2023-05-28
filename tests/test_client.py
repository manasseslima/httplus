import pytest
from skate.client import Client


@pytest.mark.asyncio
async def test_basic_client_request():
    url = ''
    client = Client()
    res = await client.get(url)
    assert res
