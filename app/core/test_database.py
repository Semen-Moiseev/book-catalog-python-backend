import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.core.database import Base

load_dotenv()
TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")

# Создаём движок для тестовой БД
test_async_engine = create_async_engine(TEST_DATABASE_URL, echo=True)

# Создаём асинхронную сессию для тестов
test_async_session_maker = sessionmaker(
	test_async_engine,
	expire_on_commit=False,
	class_=AsyncSession
)

# Функция для создания таблиц в тестовой БД
async def init_test_db():
	async with test_async_engine.begin() as conn:
		await conn.run_sync(Base.metadata.create_all)
