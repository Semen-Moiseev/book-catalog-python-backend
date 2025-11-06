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
		return genre

	@staticmethod
	async def create_genre(genre_data: GenreCreate):
		# Проверяем уникальность имени
		await check_unique_genre_name_for_create(genre_data.name)
		genre = await GenreRepository.create(genre_data)
		return genre


	@staticmethod
	async def update_genre(genre_id: int, update_data: GenreUpdate):
		# Проверяем уникальность имени
		await check_unique_genre_name_for_update(genre_id, update_data.name)
		genre = await GenreRepository.update(genre_id, update_data)
		return genre

	@staticmethod
	async def delete_genre(genre_id: int):
		return await GenreRepository.delete(genre_id)

async def check_unique_genre_name_for_create(name: str):
	existing = await GenreRepository.get_by_name(name)
	if existing:
		raise HTTPException(
			status_code=400,
			detail=f"Genre with name '{name}' already exists."
		)

async def check_unique_genre_name_for_update(genre_id: int, name: str):
	async with async_session() as session:
		result = await session.execute(
			select(Genre).where(Genre.name == name, Genre.id != genre_id)
		)
		existing_author = result.scalar_one_or_none()
		if existing_author:
			raise HTTPException(
				status_code=400,
				detail=f"Genre with name '{name}' already exists."
			)