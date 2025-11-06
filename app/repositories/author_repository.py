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
