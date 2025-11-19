from app.repositories.base_repository import SQLAlchemyRepository
from app.models.book import Book
from app.schemas.book import BookCreate, BookUpdate
from app.models.genre import Genre
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

class BookRepository(SQLAlchemyRepository[Book, BookCreate, BookUpdate]):
	model = Book


	async def list_all(self, page: int, per_page: int):
		total_result = await self.session.execute(select(func.count()).select_from(Book))
		total = total_result.scalar() or 0

		stmt = (
			select(Book)
			.options(selectinload(Book.genres))
			.offset((page - 1) * per_page)
			.limit(per_page)
		)
		res = await self.session.execute(stmt)
		items = res.scalars().all()

		return {
			"page": page,
			"per_page": per_page,
			"total": total,
			"total_pages": (total + per_page - 1) // per_page,
			"items": items,
		}


	async def get_by_id(self, id: int) -> Book | None:
		stmt = select(Book).options(selectinload(Book.genres)).where(Book.id == id)
		res = await self.session.execute(stmt)
		return res.scalar_one_or_none()


	async def create(self, data: dict, genres: list[Genre]) -> Book:
		book = Book(**data)
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


	async def update(self, instance: Book, data: BookUpdate) -> Book:
		data = data.model_dump(exclude_unset=True)

		for key in ["title", "type", "author_id"]:
			if key in data:
				setattr(instance, key, data[key])

		if "genres" in data:
			genre_ids = data["genres"]
			stmt = select(Genre).where(Genre.id.in_(genre_ids))
			res = await self.session.execute(stmt)
			genres = res.scalars().all()
			instance.genres = genres

		self.session.add(instance)
		await self.session.commit()
		await self.session.refresh(instance)

		result = await self.session.execute(
			select(Book)
			.options(selectinload(Book.genres))
			.where(Book.id == instance.id)
		)
		book_with_genres = result.scalar_one()

		return book_with_genres


	async def check_unique_name(self, title: str, author_id: int) -> bool:
		stmt = select(Genre).where(Book.title == title, Book.author_id == author_id)
		result = await self.session.execute(stmt)
		return result.scalars().first() is None