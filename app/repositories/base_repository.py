from abc import ABC, abstractmethod
from sqlalchemy import select, func
from typing import Generic, TypeVar, Type
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

ModelType = TypeVar("ModelType") # ORM-модель
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel) # Схема создания
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel) # Схема обновления

class AbstractRepository(ABC, Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
	model: Type[ModelType]


	def __init__(self, session: AsyncSession):
		self.session = session

	@abstractmethod
	async def list_all(self, page: int, per_page: int): ...

	@abstractmethod
	async def get_by_id(self, id: int) -> ModelType | None: ...

	@abstractmethod
	async def create(self, data: CreateSchemaType) -> ModelType: ...

	@abstractmethod
	async def update(self, instance: ModelType, data: UpdateSchemaType) -> ModelType: ...

	@abstractmethod
	async def delete(self, instance: ModelType): ...


class SQLAlchemyRepository(AbstractRepository[ModelType, CreateSchemaType, UpdateSchemaType]):
	async def list_all(self, page: int, per_page: int):
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


	async def get_by_id(self, id: int) -> ModelType | None:
		stmt = select(self.model).where(self.model.id == id)
		res = await self.session.execute(stmt)
		return res.scalar_one_or_none()


	async def create(self, data: CreateSchemaType) -> ModelType:
		instance = self.model(**data)
		self.session.add(instance)
		await self.session.commit()
		await self.session.refresh(instance)
		return instance


	async def update(self, instance: ModelType, data: UpdateSchemaType) -> ModelType:
		for key, value in data.model_dump(exclude_unset=True).items():
			if value is not None:
				setattr(instance, key, value)
		self.session.add(instance)
		await self.session.commit()
		await self.session.refresh(instance)
		return instance


	async def delete(self, instance: ModelType):
		await self.session.delete(instance)
		await self.session.commit()