from app.services.base_service import BaseService
from app.schemas.book import BookCreate, BookUpdate
from fastapi import HTTPException
from app.repositories.genre_repository import GenreRepository
from app.repositories.book_repository import BookRepository

class BookService(BaseService):
	def __init__(self, book_repo: BookRepository, genre_repo: GenreRepository | None = None):
		super().__init__(book_repo)
		self.genre_repo = genre_repo


	async def create(self, data: BookCreate):
		# Проверка уникальности ...

		genres = []
		if data.genres:
			genres = await self.genre_repo.get_by_ids(data.genres)
			if not genres:
				raise HTTPException(status_code=400, detail="Invalid genres")

		return await self.repository.create(data.model_dump(exclude={"genres"}), genres=genres)


	async def update(self, book_id: int, update_data: BookUpdate):
		book = await self.get_by_id(book_id)
		# Проверка уникальности ...

		return await self.repository.update(book, update_data)