import pytest
from httpx import AsyncClient


@pytest.mark.parametrize('email, password, status_code', [
    ('kot@kot.com', 'kotkot', 200),
    ('kot@kot.com', 'kotkot1', 409),
    ('qwerty', 'kotkot', 422)
])
async def test_register_user(email, password, status_code, ac: AsyncClient):
    response = await ac.post('/auth/register', json={
        'email': email,
        'password': password})
    assert response.status_code == status_code


@pytest.mark.parametrize('email, password, status_code', [
    ('test@test.com', 'test', 200),
    ('kot@kot.com', 'kotkot1', 401)
])
async def test_login_user(email, password, status_code, ac: AsyncClient):
    response = await ac.post('/auth/login', json={
        'email': email,
        'password': password})
    assert response.status_code == status_code


@pytest.mark.parametrize('email, password, status_code', [
    ('test@test.com', 'test', 200),
])
async def test_logout_user(email, password, status_code, ac: AsyncClient):
    await ac.post('/auth/login', json={
        'email': email,
        'password': password})
    response = await ac.post('/auth/logout')
    assert response.status_code == status_code
    assert 'task_access_token' not in response.cookies


@pytest.mark.parametrize('email, password, status_code', [
    ('test@test.com', 'test', 200),
])
async def test_read_users_me(email, password, status_code, ac: AsyncClient):
    await ac.post('/auth/login', json={
        'email': email,
        'password': password})
    response = await ac.get('/auth/me')
    assert response.status_code == status_code
    assert response.json() == email


async def test_read_users_me_negative(ac: AsyncClient):
    response = await ac.get('/auth/me')
    assert response.status_code == 401


async def test_logout_user_negative(ac: AsyncClient):
    response = await ac.post('/auth/logout')
    assert response.status_code == 401