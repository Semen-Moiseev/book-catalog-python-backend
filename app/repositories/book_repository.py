from app.core.database import async_session
from sqlalchemy.future import select
from app.models.book import Book

class BookRepository:
	@staticmethod
	async def get_all():
		async with async_session() as session:
			result = await session.execute(select(Book))
			books = result.scalars().all()
			return books
