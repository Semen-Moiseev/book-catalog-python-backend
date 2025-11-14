from app.services.base_service import BaseService
from app.schemas.genre import GenreCreate, GenreUpdate
from fastapi import HTTPException

class GenreService(BaseService):
	async def create(self, data: GenreCreate):
		if not await self.repository.check_unique_name(data.name):
			raise HTTPException(status_code=400, detail=f"Genre with name '{data.name}' already exists.")

		return await self.repository.create(data.model_dump())


	async def update(self, id: int, data: GenreUpdate):
		genre = await self.get_by_id(id)
		if not await self.repository.check_unique_name(data.name, genre_id):
			raise HTTPException(status_code=400, detail=f"Genre with name '{data.name}' already exists.")

		return await self.repository.update(genre, data)