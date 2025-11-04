from app.core.database import async_session
from sqlalchemy.future import select
from app.models.genre import Genre
from app.schemas.genre import GenreUpdate, GenreCreate

class GenreRepository:
	@staticmethod
	async def get_all():
		async with async_session() as session:
			result = await session.execute(select(Genre))
			genres = result.scalars().all()
			return genres

	@staticmethod
	async def find_by_id(genre_id: int):
		async with async_session() as session:
			result = await session.get(Genre, genre_id)
			return result

	@staticmethod
	async def create(genre_data: GenreCreate):
		async with async_session() as session:
			genre = Genre(name=genre_data.name)
			session.add(genre)
			await session.commit()
			await session.refresh(genre)
			return genre

	@staticmethod
	async def update(genre_id: int, update_data: GenreUpdate):
		async with async_session() as session:
			genre = await session.get(Genre, genre_id)
			if not genre:
				return None

			for key, value in update_data.dict(exclude_unset=True).items():
				setattr(genre, key, value)
			session.add(genre)
			await session.commit()
			await session.refresh(genre)
			return genre

	@staticmethod
	async def delete(genre_id: int):
		async with async_session() as session:
			genre = await session.get(Genre, genre_id)
			if not genre:
				return False

			await session.delete(genre)
			await session.commit()
			return True

	@staticmethod
	async def get_by_name(name: str):
		async with async_session() as session:
			result = await session.execute(select(Genre).where(Genre.name == name))
			return result.scalar_one_or_none()
