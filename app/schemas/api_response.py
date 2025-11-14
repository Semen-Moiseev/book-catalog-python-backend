from typing import TypeVar, Generic
from pydantic import BaseModel

T = TypeVar("T")

class ApiResponse(BaseModel, Generic[T]):
	success: bool = True
	code: int
	message: str
	data: T

	model_config = {
		"from_attributes": True
	}
