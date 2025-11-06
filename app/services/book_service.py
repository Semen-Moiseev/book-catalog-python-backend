from app.repositories.book_repository import BookRepository
from app.schemas.book import BookCreate, BookUpdate

class BookService:
	@staticmethod
	async def get_all_books(page, per_page):
		return await BookRepository.get_all(page, per_page)

	@staticmethod
	async def get_by_id_book(book_id: int):
		book = await BookRepository.find_by_id(book_id)
		return book

	@staticmethod
	async def create_book(book_data: BookCreate):
		# Проверка уникальности??
		book = await BookRepository.create(book_data)
		return book

	@staticmethod
	async def update_book(book_id: int, update_data: BookUpdate):
		# Проверка уникальности??
		book = await BookRepository.update(book_id, update_data)
		return book

	@staticmethod
	async def delete_book(book_id: int):
		return await BookRepository.delete(book_id)