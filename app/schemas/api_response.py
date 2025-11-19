from typing import TypeVar, Generic
from pydantic import BaseModel
from typing import Optional

T = TypeVar("T")

class ApiResponse(BaseModel, Generic[T]):
	success: bool = True
	code: int
	message: str
	data: Optional[T] = None

	model_config = {
		"from_attributes": True
	}

class ApiErrorResponse(ApiResponse[None]):
	success: bool = False
	data: None = None
