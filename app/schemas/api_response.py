from typing import TypeVar, Generic
from pydantic import BaseModel
from typing import Optional

T = TypeVar("T")

class ApiResponse(BaseModel, Generic[T]):
	success: bool
	code: int
	message: str
	data: Optional[T] = {}

	model_config = {
		"from_attributes": True
	}
