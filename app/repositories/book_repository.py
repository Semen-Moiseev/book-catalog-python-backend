from app.repositories.repository import SQLAlchemyRepository
from app.models.book import Book
from app.schemas.book import BookCreate, BookUpdate, BookResponse

class BookRepository(SQLAlchemyRepository[Book, BookCreate, BookUpdate, BookResponse]):
	model = Book
	response_schema = BookResponse