from abc import ABC, abstractmethod
from app.repositories.base_repository import AbstractRepository
from fastapi import HTTPException

class AbstractService(ABC):
	@abstractmethod
	async def list_all(self, page: int, per_page: int): ...

	@abstractmethod
	async def get_by_id(self, id: int): ...

	@abstractmethod
	async def delete(self, id: int): ...


class BaseService(AbstractService):
	def __init__(self, repository: AbstractRepository):
		self.repository = repository


	async def list_all(self, page: int, per_page: int):
		return await self.repository.list_all(page, per_page)


	async def get_by_id(self, id: int):
		entity = await self.repository.get_by_id(id)
		if not entity:
			raise HTTPException(status_code=404, detail="Item not found")
		return entity


	async def delete(self, id: int):
		entity = await self.repository.get_by_id(id)
		if not entity:
			raise HTTPException(status_code=404, detail="Item not found")
		return await self.repository.delete(entity)