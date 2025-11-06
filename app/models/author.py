from app.core.database import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

class Author(Base):
	__tablename__ = "authors"

	id = Column(Integer, primary_key=True, index=True)
	name = Column(String(255), nullable=False)
	user_id = Column(Integer, nullable=False, index=True)

	books = relationship("Book", back_populates="author", cascade="all, delete-orphan")