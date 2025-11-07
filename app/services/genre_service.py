from app.repositories.genre_repository import GenreRepository
from app.schemas.genre import GenreCreate, GenreUpdate
from app.core.database import async_session
from sqlalchemy import select
from app.models.genre import Genre
from fastapi import HTTPException
from app.utils.repository import AbstractRepository

class GenreService:
	def __init__(self, repository: AbstractRepository):
		self.repository: AbstractRepository = repository()


	async def get_all_genres(page: int, per_page: int):
		return await GenreRepository.get_all(page, per_page)


	async def get_by_id_genre(genre_id: int):
		genre = await GenreRepository.find_by_id(genre_id)
		if not genre:
			raise HTTPException(status_code=404, detail="Genre not found")
		return genre


	async def create_genre(self, genre_data: GenreCreate):
		if not await GenreRepository.check_unique_genre_name_for_create(genre_data.name):
			raise HTTPException(status_code=400, detail=f"Genre with name '{genre_data.name}' already exists.")

		genre = await self.repository.create(genre_data.model_dump())
		return genre


	async def update_genre(genre_id: int, update_data: GenreUpdate):
		genre = await GenreRepository.find_by_id(genre_id)
		if not genre:
			raise HTTPException(status_code=404, detail="Genre not found")

		if not await GenreRepository.check_unique_genre_name_for_update(update_data.name, genre_id):
			raise HTTPException(status_code=400, detail=f"Genre with name '{update_data.name}' already exists.")

		updated_genre = await GenreRepository.update(genre, update_data)
		return updated_genre


	async def delete_genre(genre_id: int):
		genre = await GenreRepository.find_by_id(genre_id)
		if not genre:
			raise HTTPException(status_code=404, detail="Genre not found")
		return await GenreRepository.delete(genre)