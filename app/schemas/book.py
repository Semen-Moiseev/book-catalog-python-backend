from pydantic import BaseModel, Field
from typing import Optional, List
from app.enums.book_type import BookType
from app.schemas.genre import GenreResponse

class BookCreate(BaseModel):
	title: str = Field(..., min_length=1, max_length=255) #description="Название книги"
	type: BookType = Field(...)
	author_id: int = Field(...)
	genres: List[int] = []


class BookUpdate(BaseModel):
	title: Optional[str] = Field(None, min_length=1, max_length=255)
	type: Optional[BookType] = Field(None)
	author_id: Optional[int] = Field(None)
	genres: Optional[List[int]] = Field(None)


class BookResponse(BaseModel):
	id: int
	title: str
	type: BookType
	author_id: int
	genres: List[GenreResponse]

	model_config = {
		"from_attributes": True
	}

class BookListResponse(BaseModel):
	page: int
	per_page: int
	total: int
	total_pages: int
	items: List[BookResponse]

	model_config = {
		"from_attributes": True
	}
