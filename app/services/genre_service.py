from app.repositories.repository import AbstractRepository
from app.schemas.genre import GenreCreate, GenreUpdate
from fastapi import HTTPException
from app.services.service import BaseService
from app.schemas.genre import GenreCreate, GenreUpdate

class GenreService(BaseService):
	async def create(self, genre_data: GenreCreate):
		if not await self.repository.check_unique_genre_name_for_create(genre_data.name):
			raise HTTPException(status_code=400, detail=f"Genre with name '{genre_data.name}' already exists.")

		genre = await self.repository.create(genre_data.model_dump())
		return genre


	async def update(self, genre_id: int, update_data: GenreUpdate):
		genre = await self.repository.find_by_id(genre_id)
		if not genre:
			raise HTTPException(status_code=404, detail="Genre not found")

		if not await self.repository.check_unique_genre_name_for_update(update_data.name, genre_id):
			raise HTTPException(status_code=400, detail=f"Genre with name '{update_data.name}' already exists.")

		updated_genre = await self.repository.update(genre, update_data)
		return updated_genre