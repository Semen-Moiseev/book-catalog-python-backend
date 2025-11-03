from sqlmodel import SQLModel, Field
from typing import Optional

class Author(SQLModel, table=True):
	__tablename__ = "authors"
	id: Optional[int] = Field(default=None, primary_key=True)
	name: str
	user_id: int