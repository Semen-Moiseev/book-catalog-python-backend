from app.repositories.repository import SQLAlchemyRepository
from app.models.book import Book
from app.schemas.book import BookCreate, BookUpdate, BookResponse
from app.models.genre import Genre
from sqlalchemy import select
from sqlalchemy.orm import selectinload

class BookRepository(SQLAlchemyRepository[Book, BookCreate, BookUpdate, BookResponse]):
	model = Book
	response_schema = BookResponse

	async def create(self, data: dict, genres: list[Genre] = None) -> Book:
		book = self.model(**data)
		self.session.add(book)
		if genres:
			book.genres = genres

		await self.session.commit()
		await self.session.refresh(book)

		result = await self.session.execute(
			select(Book)
			.options(selectinload(Book.genres))
			.where(Book.id == book.id)
		)
		book_with_genres = result.scalar_one()

		return book_with_genres