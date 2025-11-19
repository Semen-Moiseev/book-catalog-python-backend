from app.services.base_service import BaseService
from app.models.author import Author
from app.schemas.author import AuthorUpdate
from app.core.exceptions import AppException

class AuthorService(BaseService[Author]):
	async def update(self, id: int, data: AuthorUpdate) -> Author:
		author = await self.get_by_id(id)
		if not await self.repository.check_unique_name(data.name, id):
			raise AppException(400, f"Author with name '{data.name}' already exists")

		return await self.repository.update(author, data)
