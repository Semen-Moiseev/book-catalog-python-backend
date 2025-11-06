from app.repositories.genre_repository import GenreRepository
from app.schemas.genre import GenreCreate, GenreUpdate
from app.core.database import async_session
from sqlalchemy import select
from app.models.genre import Genre
from fastapi import HTTPException

class GenreService:
	@staticmethod
	async def get_all_genres(page, per_page):
		return await GenreRepository.get_all(page, per_page)

	@staticmethod
	async def get_by_id_genre(genre_id: int):
		genre = await GenreRepository.find_by_id(genre_id)
		if not genre:
			raise HTTPException(status_code=404, detail="Genre not found")
		return genre

	@staticmethod
	async def create_genre(genre_data: GenreCreate):
		if not await GenreRepository.check_unique_genre_name_for_create(genre_data.name):
			raise HTTPException(status_code=400, detail=f"Genre with name '{genre_data.name}' already exists.")

		genre = await GenreRepository.create(genre_data)
		return genre


	@staticmethod
	async def update_genre(genre_id: int, update_data: GenreUpdate):
		genre = await GenreRepository.find_by_id(genre_id)
		if not genre:
			raise HTTPException(status_code=404, detail="Genre not found")

		if not await GenreRepository.check_unique_genre_name_for_update(update_data.name, genre_id):
			raise HTTPException(status_code=400, detail=f"Genre with name '{update_data.name}' already exists.")

		updated_genre = await GenreRepository.update(genre, update_data)
		return updated_genre

	@staticmethod
	async def delete_genre(genre_id: int):
		genre = await GenreRepository.find_by_id(genre_id)
		if not genre:
			raise HTTPException(status_code=404, detail="Genre not found")
		return await GenreRepository.delete(genre)