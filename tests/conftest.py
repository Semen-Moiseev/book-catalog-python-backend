import pytest
from httpx import AsyncClient, ASGITransport
from fastapi import FastAPI
from app.main import app
from app.core.test_database import test_async_session_maker, init_test_db

@pytest.fixture(scope="session")
async def initialized_test_db():
	# создаём таблицы в тестовой базе
	await init_test_db()
	yield

@pytest.fixture
async def client(initialized_test_db):
	async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
		yield ac
