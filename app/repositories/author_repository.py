from app.repositories.repository import SQLAlchemyRepository
from app.models.author import Author
from app.schemas.author import AuthorCreate, AuthorUpdate, AuthorResponse
from sqlalchemy import select

class AuthorRepository(SQLAlchemyRepository[Author, AuthorCreate, AuthorUpdate, AuthorResponse]):
	model = Author
	response_schema = AuthorResponse

	async def check_unique_author_name_for_update(self, name: str, author_id: int = None):
		query = select(Author).where(Author.name == name, Author.id != author_id)
		result = await self.session.execute(query)
		return result.scalar_one_or_none() is None
