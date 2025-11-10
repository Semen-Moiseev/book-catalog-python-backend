from app.repositories.repository import SQLAlchemyRepository
from app.models.genre import Genre
from app.schemas.genre import GenreCreate, GenreUpdate, GenreResponse
from sqlalchemy import select

class GenreRepository(SQLAlchemyRepository[Genre, GenreCreate, GenreUpdate, GenreResponse]):
	model = Genre
	response_schema = GenreResponse

	async def check_unique_genre_name_for_create(self, name: str):
		result = await self.session.execute(select(Genre).where(Genre.name == name))
		return result.scalar_one_or_none() is None

	async def check_unique_genre_name_for_update(self, genre_id: int, name: str):
		query = select(Genre).where(Genre.name == name, Genre.id != genre_id)
		result = await self.session.execute(query)
		return result.scalar_one_or_none() is None
