from sqlalchemy import Table, Column, ForeignKey
from app.core.database import Base

book_genre = Table(
	"book_genre",
	Base.metadata,
	Column("book_id", ForeignKey("books.id", ondelete="CASCADE"), primary_key=True),
	Column("genre_id", ForeignKey("genres.id", ondelete="CASCADE"), primary_key=True)
)
