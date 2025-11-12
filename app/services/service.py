from abc import ABC, abstractmethod
from app.repositories.repository import AbstractRepository
from fastapi import HTTPException

class AbstractService(ABC):
	@abstractmethod
	async def get_all(self, page: int, per_page: int): ...

	@abstractmethod
	async def get_by_id(self, genre_id: int): ...

	@abstractmethod
	async def delete(self, item_id: int): ...


class BaseService(AbstractService):
	def __init__(self, repository: AbstractRepository):
		self.repository = repository

	async def get_all(self, page: int, per_page: int):
		return await self.repository.get_all(page, per_page)

	async def get_by_id(self, genre_id: int):
		obj = await self.repository.find_by_id(genre_id)
		if not obj:
			raise HTTPException(status_code=404, detail="Item not found")
		return obj

	async def delete(self, item_id: int):
		obj = await self.repository.find_by_id(item_id)
		if not obj:
			raise HTTPException(status_code=404, detail="Item not found")
		return await self.repository.delete(obj)