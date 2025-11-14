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
		if not await self.repository.check_unique_name(data.title, data.author_id):
			raise HTTPException(status_code=400, detail=f"Book with title '{data.title}' already exists.")

		genres = []
		if data.genres:
			genres = await self.genre_repo.get_by_ids(data.genres)
			if not genres:
				raise HTTPException(status_code=400, detail="Invalid genres")

		return await self.repository.create(data.model_dump(exclude={"genres"}), genres=genres)


	async def update(self, id: int, data: BookUpdate):
		book = await self.get_by_id(id)
		if not await self.repository.check_unique_name(data.title, data.author_id):
			raise HTTPException(status_code=400, detail=f"Book with title '{data.title}' already exists.")

		return await self.repository.update(book, data)