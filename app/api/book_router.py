from fastapi import APIRouter, status, HTTPException, Query
from app.services.book_service import BookService
from app.core.response_builder import success_response
from typing import List
from app.schemas.book import BookResponse
from app.schemas.book import BookCreate, BookUpdate

router = APIRouter(prefix="/books", tags=["Books"])

@router.get("/", response_model=List[BookResponse], status_code=status.HTTP_200_OK)
async def list_books(
	page: int = Query(1, ge=1),
	per_page: int = Query(5, ge=1, le=100)):
	books = await BookService.get_all_books(page, per_page)
	return success_response(books, "Books fetched successfully")

@router.get("/{book_id}", response_model=List[BookResponse], status_code=status.HTTP_200_OK)
async def get_book(book_id: int):
	book = await BookService.get_by_id_book(book_id)
	if not book:
		raise HTTPException(status_code=404, detail="Book not found")

	book_data = BookResponse.model_validate(book).model_dump()
	return success_response(book_data, "The data was successfully found")

@router.post("/", response_model=List[BookResponse], status_code=status.HTTP_200_OK)
async def create_book(book_create: BookCreate):
	created_book = await BookService.create_book(book_create)
	if not created_book:
		raise HTTPException(status_code=404, detail="Book not found")

	book_data = BookResponse.model_validate(created_book).model_dump()
	return success_response(book_data, "The data has been successfully created")

@router.put("/{book_id}", response_model=List[BookResponse], status_code=status.HTTP_200_OK)
async def update_book(book_id: int, book_update: BookUpdate):
	updated_book = await BookService.update_book(book_id, book_update)
	if not updated_book:
		raise HTTPException(status_code=404, detail="Book not found")

	book_data = BookResponse.model_validate(updated_book).model_dump()
	return success_response(book_data, "The data has been successfully updated")

@router.delete("/{book_id}")
async def delete_book(book_id: int):
	deleted = await BookService.delete_book(book_id)
	if not deleted:
		raise HTTPException(status_code=404, detail="Book not found")

	return success_response(None, "The data has been successfully deleted")