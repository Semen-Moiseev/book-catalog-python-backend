from app.services.base_service import BaseService
from app.schemas.author import AuthorUpdate
from fastapi import HTTPException

class AuthorService(BaseService):
	async def update(self, id: int, data: AuthorUpdate):
		author = await self.get_by_id(id)
		if not await self.repository.check_unique_name(data.name, author_id):
			raise HTTPException(status_code=400, detail=f"Author with name '{data.name}' already exists")

		return await self.repository.update(author, data)
