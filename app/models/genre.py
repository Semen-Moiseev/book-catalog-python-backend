from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.models import book_genre
from app.core.database import Base

class Genre(Base):
	__tablename__ = "genres"

	id = Column(Integer, primary_key=True, index=True)
	name = Column(String(255), nullable=False)

	books = relationship("Book", secondary=book_genre, back_populates="genres")