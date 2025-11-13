from app.core.database import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.models import book_genre

class Genre(Base):
	__tablename__ = "genres"

	id = Column(Integer, primary_key=True)
	name = Column(String(255), nullable=False)

	books = relationship("Book", secondary=book_genre, back_populates="genres")

	def __repr__(self):
		return f"<Genre(id={self.id}, name='{self.name}')>"