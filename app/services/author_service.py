from app.repositories.author_repository import AuthorRepository
from app.schemas.author import AuthorUpdate
from fastapi import HTTPException
from sqlalchemy import select
from app.core.database import async_session
from app.models.author import Author

class AuthorService:

	@staticmethod
	async def get_all_authors():
		return await AuthorRepository.get_all()

	@staticmethod
	async def get_by_id_author(author_id: int):
		author = await AuthorRepository.find_by_id(author_id)
		return author

	@staticmethod
	async def update_author(author_id: int, update_data: AuthorUpdate):
		# Проверяем уникальность имени
		await check_unique_author_name(author_id, update_data.name)

		author = await AuthorRepository.update(author_id, update_data)
		return author

	@staticmethod
	async def delete_author(author_id: int):
		return await AuthorRepository.delete(author_id)

async def check_unique_author_name(author_id: int, name: str):
	async with async_session() as session:
		result = await session.execute(
			select(Author).where(Author.name == name, Author.id != author_id)
		)
		existing_author = result.scalar_one_or_none()
		if existing_author:
			raise HTTPException(
				status_code=400,
				detail=f"Author with name '{name}' already exists."
			)