from app.repositories.repository import SQLAlchemyRepository
from app.models.genre import Genre
from app.schemas.genre import GenreCreate, GenreUpdate
from sqlalchemy import select

class GenreRepository(SQLAlchemyRepository[Genre, GenreCreate, GenreUpdate]):
	model = Genre


	async def check_unique_genre_name_for_create(self, name: str):
		stmt = select(Genre).where(Genre.name == name)
		result = await self.session.execute(stmt)
		return result.scalar_one_or_none() is None


	async def check_unique_genre_name_for_update(self, genre_id: int, name: str):
		stmt = select(Genre).where(Genre.name == name, Genre.id != genre_id)
		result = await self.session.execute(stmt)
		return result.scalar_one_or_none() is None


	async def get_by_ids(self, genres: list[int]):
		stmt = select(Genre).where(Genre.id.in_(genres))
		result = await self.session.execute(stmt)
		return result.scalars().all()
