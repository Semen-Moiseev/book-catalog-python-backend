from app.repositories.base_repository import SQLAlchemyRepository
from app.models.genre import Genre
from app.schemas.genre import GenreCreate, GenreUpdate
from sqlalchemy import select

class GenreRepository(SQLAlchemyRepository[Genre, GenreCreate, GenreUpdate]):
	model = Genre


	async def check_unique_name(self, name: str, id: int | None = None):
		if id:
			stmt = select(Genre).where(Genre.name == name, Genre.id != id)
		else:
			stmt = select(Genre).where(Genre.name == name)
		result = await self.session.execute(stmt)
		return result.scalar_one_or_none() is None


	async def get_by_ids(self, genres: list[int]):
		stmt = select(Genre).where(Genre.id.in_(genres))
		result = await self.session.execute(stmt)
		return result.scalars().all()
