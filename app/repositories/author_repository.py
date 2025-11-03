from app.core.database import async_session
from app.models.author import Author
from sqlalchemy.future import select

class AuthorRepository:

	@staticmethod
	async def get_all():
		async with async_session() as session:
			result = await session.execute(select(Author))
			authors = result.scalars().all()
			return authors