from fastapi import APIRouter, status, HTTPException
from app.services.book_service import BookService
from app.core.response_builder import success_response
from typing import List
from app.schemas.book import BookResponse
from app.schemas.author import AuthorUpdate

router = APIRouter(prefix="/books", tags=["Books"])

@router.get("/", response_model=List[BookResponse], status_code=status.HTTP_200_OK)
async def list_books():
	books = await BookService.get_all_books()
	books_data = [BookResponse.model_validate(book).model_dump() for book in books]
	return success_response(books_data, "Books fetched successfully")