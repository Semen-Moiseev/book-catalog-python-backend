from app.core.database import async_session
from sqlalchemy import select, func
from app.models.genre import Genre
from app.schemas.genre import GenreUpdate, GenreCreate
from app.schemas.genre import GenreResponse

class GenreRepository:
	@staticmethod
	async def get_all(page, per_page):
		async with async_session() as session:
			total_result = await session.execute(select(func.count()).select_from(Genre))
			total = total_result.scalar() or 0

			result = await session.execute(
				select(Genre)
				.offset((page - 1) * per_page)
				.limit(per_page)
			)
			genres = result.scalars().all()

			return {
				"page": page,
				"per_page": per_page,
				"total": total,
				"total_pages": (total + per_page - 1) // per_page,
				"items": [GenreResponse.model_validate(genre).model_dump() for genre in genres],
			}

	@staticmethod
	async def find_by_id(genre_id: int):
		async with async_session() as session:
			genre = await session.get(Genre, genre_id)
			return genre

	@staticmethod
	async def create(genre_data: GenreCreate):
		async with async_session() as session:
			genre = Genre(name=genre_data.name)
			session.add(genre)
			await session.commit()
			await session.refresh(genre)
			return genre

	@staticmethod
	async def update(genre: Genre, update_data: GenreUpdate):
		async with async_session() as session:
			for key, value in update_data.model_dump(exclude_unset=True).items():
				setattr(genre, key, value)
			session.add(genre)
			await session.commit()
			await session.refresh(genre)
			return genre

	@staticmethod
	async def delete(genre: Genre):
		async with async_session() as session:
			await session.delete(genre)
			await session.commit()

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
