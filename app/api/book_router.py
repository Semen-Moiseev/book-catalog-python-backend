from fastapi import APIRouter, status, Query
from app.core.database import async_session_maker
from app.services.book_service import BookService
from app.core.response_builder import success_response
from typing import List
from app.schemas.book import BookCreate, BookUpdate, BookResponse
from app.repositories.book_repository import BookRepository

router = APIRouter(prefix="/books", tags=["Books"])

@router.get("/", response_model=List[BookResponse], status_code=status.HTTP_200_OK, description="Получение списка книг с пагинацией")
async def list_books(
	page: int = Query(1, ge=1, description="Номер страницы"),
	per_page: int = Query(5, ge=1, le=100, description="Количество элементов на странице")
):
	async with async_session_maker() as session:
		books = await BookService(BookRepository(session)).get_all_books(page, per_page)
		return success_response(books, "Books fetched successfully")

@router.get("/{book_id}", response_model=List[BookResponse], status_code=status.HTTP_200_OK, description="Получение книги по id")
async def get_book(book_id: int):
	async with async_session_maker() as session:
		book = await BookService(BookRepository(session)).get_by_id_book(book_id)
		book_data = BookResponse.model_validate(book).model_dump()
		return success_response(book_data, "The data was successfully found")

@router.post("/", response_model=List[BookResponse], status_code=status.HTTP_200_OK, description="Создание новой книги")
async def create_book(book_create: BookCreate):
	async with async_session_maker() as session:
		created_book = await BookService(BookRepository(session)).create_book(book_create)
		book_data = BookResponse.model_validate(created_book).model_dump()
		return success_response(book_data, "The data has been successfully created")

@router.put("/{book_id}", response_model=List[BookResponse], status_code=status.HTTP_200_OK, description="Обновление книги по id")
async def update_book(book_id: int, book_update: BookUpdate):
	async with async_session_maker() as session:
		updated_book = await BookService(BookRepository(session)).update_book(book_id, book_update)
		book_data = BookResponse.model_validate(updated_book).model_dump()
		return success_response(book_data, "The data has been successfully updated")

@router.delete("/{book_id}", description="Удаление книги по id")
async def delete_book(book_id: int):
	async with async_session_maker() as session:
		await BookService(BookRepository(session)).delete_book(book_id)
		return success_response({}, "The data has been successfully deleted")