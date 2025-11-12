from app.services.service import BaseService
from app.schemas.book import BookCreate, BookUpdate
from fastapi import HTTPException

class BookService(BaseService):
	async def create(self, book_data: BookCreate):
		# Проверка уникальности ...

		book = await self.repository.create(book_data.model_dump())
		return book


	async def update(self, book_id: int, update_data: BookUpdate):
		book = await self.repository.find_by_id(book_id)
		if not book:
			raise HTTPException(status_code=404, detail="Book not found")

		# Проверка уникальности ...

		return await self.repository.update(book, update_data)