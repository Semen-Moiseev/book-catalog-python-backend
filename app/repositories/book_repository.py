from app.core.database import async_session
from sqlalchemy import select, func
from app.models.book import Book
from app.schemas.book import BookUpdate, BookCreate
from app.schemas.book import BookResponse

class BookRepository:
	@staticmethod
	async def get_all(page, per_page):
		async with async_session() as session:
			total_result = await session.execute(select(func.count()).select_from(Book))
			total = total_result.scalar() or 0

			result = await session.execute(
				select(Book)
				.offset((page - 1) * per_page)
				.limit(per_page)
			)
			books = result.scalars().all()

			return {
				"page": page,
				"per_page": per_page,
				"total": total,
				"total_pages": (total + per_page - 1) // per_page,
				"items": [BookResponse.model_validate(book).model_dump() for book in books],
			}

	@staticmethod
	async def find_by_id(book_id: int):
		async with async_session() as session:
			book = await session.get(Book, book_id)
			return book

	@staticmethod
	async def create(book_data: BookCreate):
		async with async_session() as session:
			book = Book(title=book_data.title, type=book_data.type, author_id=book_data.author_id)
			session.add(book)
			await session.commit()
			await session.refresh(book)
			return book

	@staticmethod
	async def update(book: Book, update_data: BookUpdate):
		async with async_session() as session:
			for key, value in update_data.model_dump(exclude_unset=True).items():
				setattr(book, key, value)
			session.add(book)
			await session.commit()
			await session.refresh(book)
			return book

	@staticmethod
	async def delete(book: Book):
		async with async_session() as session:
			await session.delete(book)
			await session.commit()
