from app.core.database import async_session
from app.models.author import Author
from sqlalchemy.future import select
from app.schemas.author import AuthorUpdate

class AuthorRepository:
	@staticmethod
	async def get_all():
		async with async_session() as session:
			result = await session.execute(select(Author))
			authors = result.scalars().all()
			return authors

	@staticmethod
	async def find_by_id(author_id: int):
		async with async_session() as session:
			result = await session.get(Author, author_id)
			return result

	@staticmethod
	async def update(author_id: int, update_data: AuthorUpdate):
		async with async_session() as session:
			author = await session.get(Author, author_id)
			if not author:
				return None

			for key, value in update_data.dict(exclude_unset=True).items():
				setattr(author, key, value)
			session.add(author)
			await session.commit()
			await session.refresh(author)
			return author

	@staticmethod
	async def delete(author_id: int):
		async with async_session() as session:
			author = await session.get(Author, author_id)
			if not author:
				return False

			await session.delete(author)
			await session.commit()
			return True
