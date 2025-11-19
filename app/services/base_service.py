from typing import Generic, TypeVar
from abc import ABC, abstractmethod
from app.repositories.base_repository import AbstractRepository
from app.core.exceptions import AppException

ModelType = TypeVar("ModelType")

class AbstractService(ABC, Generic[ModelType]):
	@abstractmethod
	async def list_all(self, page: int, per_page: int): ...

	@abstractmethod
	async def get_by_id(self, id: int) -> ModelType: ...

	@abstractmethod
	async def delete(self, id: int): ...


class BaseService(AbstractService[ModelType]):
	def __init__(self, repository: AbstractRepository):
		self.repository = repository


	async def list_all(self, page: int, per_page: int):
		return await self.repository.list_all(page, per_page)


	async def get_by_id(self, id: int) -> ModelType:
		entity = await self.repository.get_by_id(id)
		if not entity:
			raise AppException(404, "Item not found")
		return entity


	async def delete(self, id: int):
		entity = await self.get_by_id(id)
		await self.repository.delete(entity)