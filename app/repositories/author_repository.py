from app.repositories.base_repository import SQLAlchemyRepository
from app.models.author import Author
from app.schemas.author import AuthorCreate, AuthorUpdate
from sqlalchemy import select

class AuthorRepository(SQLAlchemyRepository[Author, AuthorCreate, AuthorUpdate]):
	model = Author


	async def check_unique_name(self, name: str, id: int | None = None) -> bool:
		if id:
			stmt = select(Author).where(Author.name == name, Author.id != id)
		else:
			stmt = select(Author).where(Author.name == name)
		result = await self.session.execute(stmt)
		return result.scalar_one_or_none() is None
