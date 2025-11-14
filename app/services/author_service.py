from app.services.base_service import BaseService
from app.schemas.author import AuthorUpdate
from fastapi import HTTPException

class AuthorService(BaseService):
	async def update(self, author_id: int, update_data: AuthorUpdate):
		author = await self.get_by_id(author_id)
		if not await self.repository.check_unique_name(update_data.name, author_id):
			raise HTTPException(status_code=400, detail=f"Author with name '{update_data.name}' already exists.")

		return await self.repository.update(author, update_data)
