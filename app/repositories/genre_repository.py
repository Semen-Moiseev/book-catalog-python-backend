from app.models.genre import Genre
from app.utils.repository import SQLAlchemyRepository
from app.schemas.genre import GenreCreate, GenreUpdate, GenreResponse

from app.core.database import async_session
from sqlalchemy import select

class GenreRepository(SQLAlchemyRepository[Genre, GenreCreate, GenreUpdate, GenreResponse]):
	model = Genre
	response_schema = GenreResponse

	@staticmethod
	async def check_unique_genre_name_for_create(name: str):
		async with async_session() as session:
			result = await session.execute(select(Genre).where(Genre.name == name))
			return result.scalar_one_or_none() is None

	@staticmethod
	async def check_unique_genre_name_for_update(genre_id: int, name: str):
		async with async_session() as session:
			query = select(Genre).where(Genre.name == name, Genre.id != genre_id)
			result = await session.execute(query)
			return result.scalar_one_or_none() is None
