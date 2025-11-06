from app.core.database import async_session
from app.models.author import Author
from sqlalchemy import select, func
from app.schemas.author import AuthorUpdate
from app.schemas.author import AuthorResponse

class AuthorRepository:
	@staticmethod
	async def get_all(page, per_page):
		async with async_session() as session:
			total_result = await session.execute(select(func.count()).select_from(Author))
			total = total_result.scalar() or 0

			result = await session.execute(
				select(Author)
				.offset((page - 1) * per_page)
				.limit(per_page)
			)
			authors = result.scalars().all()

			return {
				"page": page,
				"per_page": per_page,
				"total": total,
				"total_pages": (total + per_page - 1) // per_page,
				"items": [AuthorResponse.model_validate(author).model_dump() for author in authors],
			}

	@staticmethod
	async def find_by_id(author_id: int) -> Author | None:
		async with async_session() as session:
			author = await session.get(Author, author_id)
			return author

	@staticmethod
	async def update(author: Author, update_data: AuthorUpdate) -> Author:
		async with async_session() as session:
			for key, value in update_data.model_dump(exclude_unset=True).items():
				setattr(author, key, value)
			session.add(author)
			await session.commit()
			await session.refresh(author)
			return author

	@staticmethod
	async def delete(author: Author):
		async with async_session() as session:
			await session.delete(author)
			await session.commit()

	@staticmethod
	async def check_unique_author_name_for_update(name: str, author_id: int = None) -> bool:
		async with async_session() as session:
			query = select(Author).where(Author.name == name, Author.id != author_id)
			result = await session.execute(query)
			return result.scalar_one_or_none() is None
