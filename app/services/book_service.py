from app.repositories.book_repository import BookRepository

class BookService:
	@staticmethod
	async def get_all_books():
		return await BookRepository.get_all()