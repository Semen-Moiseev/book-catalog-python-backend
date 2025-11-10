from abc import ABC, abstractmethod
from sqlalchemy import select, func, insert
from typing import Generic, TypeVar, Type, Optional
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

TModel = TypeVar("TModel") # ORM-модель
TCreate = TypeVar("TCreate", bound=BaseModel) # Схема создания
TUpdate = TypeVar("TUpdate", bound=BaseModel) # Схема обновления
TResponse = TypeVar("TResponse", bound=BaseModel) # Схема ответа

class AbstractRepository(ABC, Generic[TModel, TCreate, TUpdate, TResponse]):
	model: Type[TModel]
	response_schema: Optional[Type[TResponse]] = None

	def __init__(self, session: AsyncSession):
		self.session: AsyncSession = session

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
		total_result = await self.session.execute(select(func.count()).select_from(self.model))
		total = total_result.scalar() or 0

		stmt = select(self.model).offset((page - 1) * per_page).limit(per_page)
		res = await self.session.execute(stmt)
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
		stmt = select(self.model).where(self.model.id == item_id)
		res = await self.session.execute(stmt)
		return res.scalar_one_or_none() #

	async def create(self, data: TCreate):
		stmt = insert(self.model).values(**data)
		res = await self.session.execute(stmt)
		await self.session.commit()

		stmt = select(self.model).where(self.model.id == res.lastrowid)
		res = await self.session.execute(stmt)
		return res.scalar_one() #

	async def update(self, obj: TModel, update_data: TUpdate):
		for key, value in update_data.model_dump(exclude_unset=True).items():
			setattr(obj, key, value)
		self.session.add(obj)
		await self.session.commit()
		await self.session.refresh(obj)

		if self.response_schema:
			return self.response_schema.model_validate(obj).model_dump()
		return obj

	async def delete(self, obj: TModel):
		await self.session.delete(obj)
		await self.session.commit()