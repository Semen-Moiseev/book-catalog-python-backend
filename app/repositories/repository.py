from abc import ABC, abstractmethod
from sqlalchemy import select, func, insert
from typing import Generic, TypeVar, Type
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

Model = TypeVar("Model") # ORM-модель
Create = TypeVar("Create", bound=BaseModel) # Схема создания
Update = TypeVar("Update", bound=BaseModel) # Схема обновления

class AbstractRepository(ABC, Generic[Model, Create, Update]):
	model: Type[Model]

	def __init__(self, session: AsyncSession):
		self.session = session

	@abstractmethod
	async def get_all(self, page: int, per_page: int): ...

	@abstractmethod
	async def find_by_id(self, item_id: int): ...

	@abstractmethod
	async def create(self, data: Create): ...

	@abstractmethod
	async def update(self, obj: Model, update_data: Update): ...

	@abstractmethod
	async def delete(self, obj: Model): ...


class SQLAlchemyRepository(AbstractRepository[Model, Create, Update]):
	async def get_all(self, page: int, per_page: int):
		total_result = await self.session.execute(select(func.count()).select_from(self.model))
		total = total_result.scalar() or 0

		stmt = select(self.model).offset((page - 1) * per_page).limit(per_page)
		res = await self.session.execute(stmt)
		items = res.scalars().all()
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
		return res.scalar_one_or_none()


	async def create(self, data: Create):
		stmt = insert(self.model).values(**data)
		res = await self.session.execute(stmt)
		await self.session.commit()

		stmt = select(self.model).where(self.model.id == res.lastrowid)
		res = await self.session.execute(stmt)
		return res.scalar_one()


	async def update(self, obj: Model, update_data: Update):
		for key, value in update_data.model_dump(exclude_unset=True).items():
			if value is not None:
				setattr(obj, key, value)
		self.session.add(obj)
		await self.session.commit()
		await self.session.refresh(obj)
		return obj


	async def delete(self, obj: Model):
		await self.session.delete(obj)
		await self.session.commit()