import asyncio
import json

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy import insert

from app.config import settings
from app.database import Base, async_session_maker, engine
from app.main import app as fastapi_app
from app.users.models import Users


@pytest.fixture(scope='session', autouse=True)
async def prepare_database():
    assert settings.MODE == 'TEST'

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    def open_mock_json(model: str):
        with open(f'app/tests/mock_{model}.json', encoding='utf-8') as file:
            return json.load(file)

    users = open_mock_json('users')

    async with async_session_maker() as session:
        for Model, values in [
            (Users, users),
        ]:
            query = insert(Model).values(values)
            await session.execute(query)

        await session.commit()


# Taken from pytest-asyncio doc
@pytest.fixture(scope='session')
def event_loop(request):
    """Create an instance of the default event loop for each test case"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def ac():
    async with AsyncClient(app=fastapi_app, base_url='http://test') as ac:
        yield ac


@pytest.fixture(scope='session')
async def authenticated_ac():
    async with AsyncClient(app=fastapi_app, base_url='http://test') as ac:
        await ac.post('/auth/login', json={
            'email': 'test@test.com',
            'password': 'test'
        })
        print(ac.cookies)
        assert ac.cookies['exchange_access_token']
        yield ac
