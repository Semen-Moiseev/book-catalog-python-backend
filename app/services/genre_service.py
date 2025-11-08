from app.repositories.repository import AbstractRepository
from app.repositories.genre_repository import GenreRepository
from app.schemas.genre import GenreCreate, GenreUpdate
from fastapi import HTTPException

class GenreService:
	def __init__(self, genre_repo: AbstractRepository):
		self.genre_repo: AbstractRepository = genre_repo()


	async def get_all_genres(self, page: int, per_page: int):
		return await self.genre_repo.get_all(page, per_page)


	async def get_by_id_genre(self, genre_id: int):
		genre = await self.genre_repo.find_by_id(genre_id)
		if not genre:
			raise HTTPException(status_code=404, detail="Genre not found")
		return genre


	async def create_genre(self, genre_data: GenreCreate):
		if not await GenreRepository.check_unique_genre_name_for_create(genre_data.name):
			raise HTTPException(status_code=400, detail=f"Genre with name '{genre_data.name}' already exists.")

		genre = await self.genre_repo.create(genre_data.model_dump())
		return genre


	async def update_genre(self, genre_id: int, update_data: GenreUpdate):
		genre = await self.genre_repo.find_by_id(genre_id)
		if not genre:
			raise HTTPException(status_code=404, detail="Genre not found")

		if not await GenreRepository.check_unique_genre_name_for_update(update_data.name, genre_id):
			raise HTTPException(status_code=400, detail=f"Genre with name '{update_data.name}' already exists.")

		updated_genre = await self.genre_repo.update(genre, update_data)
		return updated_genre


	async def delete_genre(self, genre_id: int):
		genre = await self.genre_repo.find_by_id(genre_id)
		if not genre:
			raise HTTPException(status_code=404, detail="Genre not found")
		return await self.genre_repo.delete(genre)