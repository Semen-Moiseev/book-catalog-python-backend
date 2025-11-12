import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# Создаём движок
async_engine = create_async_engine(DATABASE_URL, echo=True)

# Создаём асинхронную сессию
async_session_maker = sessionmaker(
	bind=async_engine,
	expire_on_commit=False,
	class_=AsyncSession
)

# Базовый класс для всех моделей
Base = declarative_base()

# Функция для создания таблиц
async def init_db():
	async with async_engine.begin() as conn:
		await conn.run_sync(Base.metadata.create_all)
