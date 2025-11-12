from app.services.service import BaseService
from app.repositories.repository import AbstractRepository
from app.schemas.author import AuthorUpdate
from fastapi import HTTPException

class AuthorService(BaseService):
	async def update(self, author_id: int, update_data: AuthorUpdate):
		author = await self.repository.find_by_id(author_id)
		if not author:
			raise HTTPException(status_code=404, detail="Author not found")

		if not await self.repository.check_unique_author_name_for_update(update_data.name, author_id):
			raise HTTPException(status_code=400, detail=f"Author with name '{update_data.name}' already exists.")

		return await self.repository.update(author, update_data)
