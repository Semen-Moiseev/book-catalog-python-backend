from pydantic import BaseModel, Field
from typing import Optional

class AuthorCreate(BaseModel):
	name: str = Field(..., min_length=2, max_length=255)
	user_id: int

class AuthorUpdate(BaseModel):
	name: Optional[str] = Field(None, min_length=2, max_length=255)
	user_id: int

class AuthorResponse(BaseModel):
	id: int
	name: str
	user_id: int

	model_config = {
		"from_attributes": True
	}