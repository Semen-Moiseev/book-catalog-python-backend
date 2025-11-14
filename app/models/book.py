from app.core.database import Base
from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from app.enums.book_type import BookType
from sqlalchemy.orm import relationship
from app.models import book_genre

class Book(Base):
	__tablename__ = "books"

	id = Column(Integer, primary_key=True)
	title = Column(String(255), nullable=False)
	type = Column(Enum(BookType, values_callable=lambda x: [e.value for e in x]), nullable=False)
	author_id = Column(Integer, ForeignKey("authors.id", ondelete="CASCADE"), nullable=False, index=True)

	author = relationship("Author", back_populates="books")
	genres = relationship("Genre", secondary=book_genre, back_populates="books")

	def __repr__(self):
		return f"<Book(id={self.id}, title='{self.title}', type='{self.type}', author_id={self.author_id})>"
