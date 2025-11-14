from app.services.base_service import BaseService
from app.schemas.genre import GenreCreate, GenreUpdate
from fastapi import HTTPException

class GenreService(BaseService):
	async def create(self, genre_data: GenreCreate):
		if not await self.repository.check_unique_name(genre_data.name):
			raise HTTPException(status_code=400, detail=f"Genre with name '{genre_data.name}' already exists.")

		return await self.repository.create(genre_data.model_dump())


	async def update(self, genre_id: int, update_data: GenreUpdate):
		genre = await self.get_by_id(genre_id)
		if not await self.repository.check_unique_name(update_data.name, genre_id):
			raise HTTPException(status_code=400, detail=f"Genre with name '{update_data.name}' already exists.")

		return await self.repository.update(genre, update_data)