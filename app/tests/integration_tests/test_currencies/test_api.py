import pytest
from httpx import AsyncClient

from app.currencies.external_api import check_currencies


@pytest.mark.parametrize('email, password, status_code', [
    ('test@test.com', 'test', 200),
    ('qwerty@me.com', 'qw', 401)
])
async def test_get_list_of_currencies(email, password, status_code, ac: AsyncClient):
    await ac.post('/auth/login', json={
        'email': email,
        'password': password
    })
    response = await ac.get('/currencies/list')
    if response:
        assert response
        assert response.status_code == status_code
        assert len(response.json())
    else:
        assert not response


@pytest.mark.parametrize('email, password, cur1, cur2', [
    ('test@test.com', 'test', 'USD', 'USD'),
    ('test@test.com', 'test', 'QWE', 'rty'),
    ('test@test.com', 'test', '', 1)
])
async def test_check_currencies(email, password, cur1, cur2, ac: AsyncClient):
    await ac.post('/auth/login', json={
        'email': email,
        'password': password
    })
    result = check_currencies(cur1, cur2)
    if result:
        assert result
    else:
        assert not result


@pytest.mark.parametrize('email, password, cur1, cur2, amount, status_code', [
    ('test@test.com', 'test', 'USD', 'USD', 2, 200),
    ('test@test.com', 'test', 'QWE', 'rty', 2, 404),
    ('test@test.com', 'test', '', 1, '', 422),
    ('test@test.com', 'test', '', 1, -1, 404)
])
async def test_convert_currency(email, password, cur1, cur2, amount, status_code, ac: AsyncClient):
    await ac.post('/auth/login', json={
        'email': email,
        'password': password
    })
    response = await ac.get('/currencies/exchange', params={
        'cur_1': cur1,
        'cur_2': cur2,
        'amount': amount
    })

    if str(response.status_code).startswith('4'):
        assert response.status_code == status_code
    else:
        assert response
        assert response.json()['result'] == amount


