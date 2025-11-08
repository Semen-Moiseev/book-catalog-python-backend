from abc import ABC, abstractmethod
from app.core.database import async_session
from sqlalchemy import select, func, insert
from typing import Generic, TypeVar, Type, Optional
from pydantic import BaseModel

TModel = TypeVar("TModel") # ORM-модель
TCreate = TypeVar("TCreate", bound=BaseModel) # Схема создания
TUpdate = TypeVar("TUpdate", bound=BaseModel) # Схема обновления
TResponse = TypeVar("TResponse", bound=BaseModel) # Схема ответа

class AbstractRepository(ABC, Generic[TModel, TCreate, TUpdate, TResponse]):
	model: Type[TModel]
	response_schema: Optional[Type[TResponse]] = None

	@abstractmethod
	async def get_all(self, page: int, per_page: int):
		raise NotImplementedError

	@abstractmethod
	async def find_by_id(self, item_id: int):
		raise NotImplementedError

	@abstractmethod
	async def create(self, data: TCreate):
		raise NotImplementedError

	@abstractmethod
	async def update(self, obj: TModel, update_data: TUpdate):
		raise NotImplementedError

	@abstractmethod
	async def delete(self, obj: TModel):
		raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository[TModel, TCreate, TUpdate, TResponse]):
	async def get_all(self, page: int, per_page: int):
		async with async_session() as session:
			total_result = await session.execute(select(func.count()).select_from(self.model))
			total = total_result.scalar() or 0

			stmt = select(self.model).offset((page - 1) * per_page).limit(per_page)
			res = await session.execute(stmt)
			items = res.scalars().all()

			if self.response_schema:
				items = [self.response_schema.model_validate(i).model_dump() for i in items]

			return {
				"page": page,
				"per_page": per_page,
				"total": total,
				"total_pages": (total + per_page - 1) // per_page,
				"items": items,
			}

	async def find_by_id(self, item_id: int):
		async with async_session() as session:
			stmt = select(self.model).where(self.model.id == item_id)
			res = await session.execute(stmt)
			return res.scalar_one_or_none() #

	async def create(self, data: TCreate):
		async with async_session() as session:
			stmt = insert(self.model).values(**data)
			res = await session.execute(stmt)
			await session.commit()

			stmt = select(self.model).where(self.model.id == res.lastrowid)
			res = await session.execute(stmt)
			return res.scalar_one() #

	async def update(self, obj: TModel, update_data: TUpdate):
		async with async_session() as session:
			for key, value in update_data.model_dump(exclude_unset=True).items():
				setattr(obj, key, value)
			session.add(obj)
			await session.commit()
			await session.refresh(obj)

			if self.response_schema:
				return self.response_schema.model_validate(obj).model_dump()
			return obj

	async def delete(self, obj: TModel):
		async with async_session() as session:
			await session.delete(obj)
			await session.commit()