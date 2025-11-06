from app.repositories.book_repository import BookRepository
from app.schemas.book import BookCreate, BookUpdate
from fastapi import HTTPException

class BookService:
	@staticmethod
	async def get_all_books(page, per_page):
		return await BookRepository.get_all(page, per_page)

	@staticmethod
	async def get_by_id_book(book_id: int):
		book = await BookRepository.find_by_id(book_id)
		if not book:
			raise HTTPException(status_code=404, detail="Book not found")
		return book

	@staticmethod
	async def create_book(book_data: BookCreate):
		# Проверка уникальности??

		book = await BookRepository.create(book_data)
		return book

	@staticmethod
	async def update_book(book_id: int, update_data: BookUpdate):
		book = await BookRepository.find_by_id(book_id)
		if not book:
			raise HTTPException(status_code=404, detail="Book not found")

		# Проверка уникальности??

		return await BookRepository.update(book, update_data)

	@staticmethod
	async def delete_book(book_id: int):
		book = await BookRepository.find_by_id(book_id)
		if not book:
			raise HTTPException(status_code=404, detail="Book not found")
		await BookRepository.delete(book)