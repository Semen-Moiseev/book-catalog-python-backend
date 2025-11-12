from pydantic import BaseModel, Field
from typing import Optional, List
from app.enums.book_type import BookType

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
	genres: List[int]

	model_config = {
		"from_attributes": True
	}
