from app.core.database import async_session
from sqlalchemy.future import select
from app.models.book import Book
from app.schemas.book import BookUpdate, BookCreate

class BookRepository:
	@staticmethod
	async def get_all():
		async with async_session() as session:
			result = await session.execute(select(Book))
			books = result.scalars().all()
			return books

	@staticmethod
	async def find_by_id(book_id: int):
		async with async_session() as session:
			result = await session.get(Book, book_id)
			return result

	@staticmethod
	async def create(book_data: BookCreate):
		async with async_session() as session:
			book = Book(title=book_data.title, type=book_data.type, author_id=book_data.author_id)
			session.add(book)
			await session.commit()
			await session.refresh(book)
			return book

	@staticmethod
	async def update(book_id: int, update_data: BookUpdate):
		async with async_session() as session:
			book = await session.get(Book, book_id)
			if not book:
				return None

			for key, value in update_data.dict(exclude_unset=True).items():
				setattr(book, key, value)
			session.add(book)
			await session.commit()
			await session.refresh(book)
			return book

	@staticmethod
	async def delete(book_id: int):
		async with async_session() as session:
			book = await session.get(Book, book_id)
			if not book:
				return False

			await session.delete(book)
			await session.commit()
			return True
