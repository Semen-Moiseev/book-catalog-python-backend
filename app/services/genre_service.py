from app.services.base_service import BaseService
from app.models.genre import Genre
from app.schemas.genre import GenreCreate, GenreUpdate
from app.core.exceptions import AppException

class GenreService(BaseService[Genre]):
	async def create(self, data: GenreCreate) -> Genre:
		if not await self.repository.check_unique_name(data.name):
			raise AppException(400, f"Genre with name '{data.name}' already exists.")

		return await self.repository.create(data.model_dump())


	async def update(self, id: int, data: GenreUpdate) -> Genre:
		genre = await self.get_by_id(id)
		if not await self.repository.check_unique_name(data.name, id):
			raise AppException(400, f"Genre with name '{data.name}' already exists.")

		return await self.repository.update(genre, data)