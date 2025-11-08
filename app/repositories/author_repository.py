from app.repositories.repository import SQLAlchemyRepository
from app.models.author import Author
from app.schemas.author import AuthorCreate, AuthorUpdate, AuthorResponse
from app.core.database import async_session
from sqlalchemy import select

class AuthorRepository(SQLAlchemyRepository[Author, AuthorCreate, AuthorUpdate, AuthorResponse]):
	model = Author
	response_schema = AuthorResponse

	@staticmethod
	async def check_unique_author_name_for_update(name: str, author_id: int = None) -> bool:
		async with async_session() as session:
			query = select(Author).where(Author.name == name, Author.id != author_id)
			result = await session.execute(query)
			return result.scalar_one_or_none() is None
