from pydantic import BaseModel, Field
from typing import Optional, List

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


class GenreListResponse(BaseModel):
	page: int
	per_page: int
	total: int
	total_pages: int
	items: List[GenreResponse]

	model_config = {
		"from_attributes": True
	}