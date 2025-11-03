from sqlmodel import SQLModel, Field
from typing import Optional

class Genre(SQLModel, table=True):
	__tablename__ = "genres"
	id: Optional[int] = Field(default=None, primary_key=True)
	name: str