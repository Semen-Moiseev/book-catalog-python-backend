from app.repositories.author_repository import AuthorRepository
from app.schemas.author import AuthorUpdate
from fastapi import HTTPException
from sqlalchemy import select
from app.core.database import async_session
from app.models.author import Author

class AuthorService:
	@staticmethod
	async def get_all_authors(page: int, per_page: int):
		return await AuthorRepository.get_all(page, per_page)

	@staticmethod
	async def get_by_id_author(author_id: int):
		author = await AuthorRepository.find_by_id(author_id)
		if not author:
			raise HTTPException(status_code=404, detail="Author not found")
		return author

	@staticmethod
	async def update_author(author_id: int, update_data: AuthorUpdate):
		author = await AuthorRepository.find_by_id(author_id)
		if not author:
			raise HTTPException(status_code=404, detail="Author not found")

		if not await AuthorRepository.check_unique_author_name_for_update(update_data.name, author_id):
			raise HTTPException(status_code=400, detail=f"Author with name '{update_data.name}' already exists.")

		return await AuthorRepository.update(author, update_data)

	@staticmethod
	async def delete_author(author_id: int):
		author = await AuthorRepository.find_by_id(author_id)
		if not author:
			raise HTTPException(status_code=404, detail="Author not found")
		await AuthorRepository.delete(author)
