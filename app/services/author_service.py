from app.repositories.repository import AbstractRepository
from app.repositories.author_repository import AuthorRepository
from app.schemas.author import AuthorUpdate
from fastapi import HTTPException

class AuthorService:
	def __init__(self, author_repo: AbstractRepository):
		self.author_repo: AbstractRepository = author_repo()


	async def get_all_authors(self, page: int, per_page: int):
		return await self.author_repo.get_all(page, per_page)


	async def get_by_id_author(self, author_id: int):
		author = await self.author_repo.find_by_id(author_id)
		if not author:
			raise HTTPException(status_code=404, detail="Author not found")
		return author


	async def update_author(self, author_id: int, update_data: AuthorUpdate):
		author = await self.author_repo.find_by_id(author_id)
		if not author:
			raise HTTPException(status_code=404, detail="Author not found")

		if not await AuthorRepository.check_unique_author_name_for_update(update_data.name, author_id):
			raise HTTPException(status_code=400, detail=f"Author with name '{update_data.name}' already exists.")

		return await self.author_repo.update(author, update_data)


	async def delete_author(self, author_id: int):
		author = await self.author_repo.find_by_id(author_id)
		if not author:
			raise HTTPException(status_code=404, detail="Author not found")
		return await self.author_repo.delete(author)
