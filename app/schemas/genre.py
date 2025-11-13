from pydantic import BaseModel, Field
from typing import Optional

class GenreCreate(BaseModel):
	name: str = Field(..., max_length=255)


class GenreUpdate(BaseModel):
	name: Optional[str] = Field(None, max_length=255)


class GenreResponse(BaseModel):
	id: int
	name: str

	model_config = {
		"from_attributes": True
	}