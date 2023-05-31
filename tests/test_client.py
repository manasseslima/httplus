import pytest
from unittest import mock
from httplus.client import Client
from .mocks import mock_connection


@mock.patch('asyncio.open_connection', mock_connection)
@pytest.mark.asyncio
async def test_get_client_request():
    url = 'http://mockserver:7777/api/girls'
    client = Client()
    res = await client.get(url)
    assert res.status == 200
    data = res.json()
    assert data[0]['first_name'] == 'Ino'
    assert data[0]['last_name'] == 'Yamanaka'


@mock.patch('asyncio.open_connection', mock_connection)
@pytest.mark.asyncio
async def test_post_request():
    url = 'http://mockserver:7777/api/girls'
    client = Client()
    data = {
        'first_name': 'Karin',
        'last_name': 'Uzumaki'
    }
    res = await client.post(url, data=data)
    assert res.status == 200
    data = res.json()
    assert data['first_name'] == 'Karin'
