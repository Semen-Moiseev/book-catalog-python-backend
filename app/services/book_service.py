from app.repositories.repository import AbstractRepository
from app.schemas.book import BookCreate, BookUpdate
from fastapi import HTTPException

class BookService:
	def __init__(self, book_repo: AbstractRepository):
		self.book_repo: AbstractRepository = book_repo


	async def get_all_books(self, page, per_page):
		return await self.book_repo.get_all(page, per_page)


	async def get_by_id_book(self, book_id: int):
		book = await self.book_repo.find_by_id(book_id)
		if not book:
			raise HTTPException(status_code=404, detail="Book not found")
		return book


	async def create_book(self, book_data: BookCreate):
		# Проверка уникальности ...

		book = await self.book_repo.create(book_data.model_dump())
		return book


	async def update_book(self, book_id: int, update_data: BookUpdate):
		book = await self.book_repo.find_by_id(book_id)
		if not book:
			raise HTTPException(status_code=404, detail="Book not found")

		# Проверка уникальности ...

		return await self.book_repo.update(book, update_data)


	async def delete_book(self, book_id: int):
		book = await self.book_repo.find_by_id(book_id)
		if not book:
			raise HTTPException(status_code=404, detail="Book not found")
		return await self.book_repo.delete(book)