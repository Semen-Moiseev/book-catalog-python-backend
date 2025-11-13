from app.core.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class Author(Base):
	__tablename__ = "authors"

	id = Column(Integer, primary_key=True)
	name = Column(String(255), nullable=False)
	user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True, index=True)

	books = relationship("Book", back_populates="author", cascade="all, delete-orphan")

	def __repr__(self):
		return f"<Author(id={self.id}, name='{self.name}')>"
